# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from ._constants  import EJavaModifiers
from ._jvm        import JVM
from ._jfield     import StaticJavaField, JavaField
from ._jmethod    import StaticJavaMethod, JavaMethod
from ._conversion import _signature_for_type, _signature_for_params, _type_names_for_params
from ._exceptions import UnknownClassException
from .            import types as jtypes


@public
class JavaClass(type):

    def __new__(cls, descriptor):

        try:
            return _class_cache[descriptor]
        except KeyError:
            from ._jobject import JavaInstance

            name_trans = JVM.jvm.JClass.name_trans
            class_name = descriptor.encode("utf-8").translate(name_trans).decode("utf-8")
            try:
                jclass = JVM.jvm.JClass.forName(class_name)
            except:
                raise UnknownClassException(descriptor)

            # Determine the alternate types for this class

            # Best option is the type itself
            alternates = ["L{};".format(descriptor)]

            # Next preference is an interfaces
            try:
                java_interfaces = jclass.getInterfaces()
            except:
                raise RuntimeError("Couldn't get interfaces for '{}'".format(descriptor))
            for java_interface in java_interfaces:
                name = str(java_interface.getName())
                alternates.append("L{};".format(name.replace('.', '/')))

            # Then check all the superclasses
            java_superclass = jclass
            while True:
                java_superclass = java_superclass.getSuperclass()
                if not java_superclass: # <AK> was: java_superclass.value is None
                    break
                name = str(java_superclass.getName())
                alternates.append("L{};".format(name.replace('.', '/')))

            with JVM.jvm as (_, jenv):
                __javaclass__ = jtypes.cast(jenv.NewGlobalRef(jclass.handle), jtypes.jclass)

            # Cache the class instance, so we don't have to recreate it
            bases = (JavaInstance,)
            name  = descriptor
            attrs = dict(_descriptor=descriptor,
                         __javaclass__=__javaclass__,
                         _alternates=alternates,
                         _constructors=None,
                         _members={
                             "fields":  {},
                             "methods": {},
                         },
                         _static={
                             "fields":  {},
                             "methods": {},
                         })
            _class_cache[descriptor] = java_class = super(JavaClass, cls).__new__(cls,
                                                          str(name), bases, attrs)
            return java_class

    def __getattr__(self, name):

        class_dict = self.__dict__

        # First, try to find a field match
        try:
            field_wrapper = class_dict["_static"]["fields"][name]
        except KeyError:
            field_wrapper = class_dict["_static"]["fields"][name] = _cache_field(self, name, True)

        if field_wrapper:
            return field_wrapper.get()

        # Then try to find a method match
        try:
            method_wrapper = class_dict["_static"]["methods"][name]
        except KeyError:
            method_wrapper = class_dict["_static"]["methods"][name] = _cache_methods(self, name, True)

        if method_wrapper:
            return method_wrapper

        # If that didn't work, try an attribute on the object itself
        # try:
        #     return super(JavaClass, self).__getattribute__(name)
        # except AttributeError:
        raise AttributeError("Java class '{}' has no attribute '{}'".format(
                             class_dict["_descriptor"], name))

    def __setattr__(self, name, value):

        class_dict = self.__dict__

        # Try to find a field match
        try:
            field_wrapper = class_dict["_static"]["fields"][name]
        except KeyError:
            field_wrapper = class_dict["_static"]["fields"][name] = _cache_field(self, name, True)

        if field_wrapper:
            return field_wrapper.set(value)

        raise AttributeError("Java class '{}' has no attribute '{}'".format(
                             class_dict["_descriptor"], name))

    def __repr__(self):

        return "<JavaClass: {}>".format(self._descriptor)


@public
class JavaInterface(type):

    def __new__(cls, *args):

        if len(args) == 1:
            from ._jproxy import JavaProxy
            descriptor, = args
            name  = descriptor
            bases = (JavaProxy,)
            attrs = {}
        else:
            name, bases, attrs = args
            descriptor = bases[-1].__dict__["_descriptor"]
        attrs.update(_descriptor=descriptor,
                     _alternates=["L{};".format(descriptor)],
                     _methods={})
        java_class = super(JavaInterface, cls).__new__(cls, str(name), bases, attrs)

        name_trans = JVM.jvm.JClass.name_trans
        class_name = descriptor.encode("utf-8").translate(name_trans).decode("utf-8")
        try:
            jclass = JVM.jvm.JClass.forName(class_name)
        except:
            raise UnknownClassException(descriptor)

        with JVM.jvm as (_, jenv):
            java_class.__javaclass__ = jtypes.cast(jenv.NewGlobalRef(jclass.handle), jtypes.jclass)
            if not java_class.__javaclass__: # <AK> was: if jclass.value is None:
                raise RuntimeError("Unable to create global reference to interface.")

        # Load the methods for the class

        try:
            java_methods = jclass.getMethods()
        except:
            raise RuntimeError("Couldn't get methods for '{}'".format(descriptor))
        for java_method in java_methods:
            modifiers = java_method.getModifiers()
            is_public = EJavaModifiers.PUBLIC in modifiers
            is_static = EJavaModifiers.STATIC in modifiers
            if is_public and not is_static:
                method_name   = str(java_method.getName())
                method_params = java_method.getParameterTypes()
                type_names = _type_names_for_params(method_params)
                java_class._methods.setdefault(method_name, set()).add(type_names)

        return java_class

    def __repr__(self):

        return "<JavaInterface: {}>".format(self._descriptor)


@public
@annotate(java_class=JavaClass, static=bool)
def _cache_field(java_class, name, static):

    jclass = JVM.jvm.JClass(None, java_class.__javaclass__, borrowed=True)

    try:
        java_field = jclass.getField(name)
    except: # NoSuchFieldException
        return None

    modifiers = java_field.getModifiers()
    is_public = EJavaModifiers.PUBLIC in modifiers
    is_static = EJavaModifiers.STATIC in modifiers
    if not is_public or is_static != static:
        return None

    field_type = java_field.getType()

    signature = _signature_for_type(field_type)
    if static:
        wrapper = StaticJavaField(java_class=java_class, name=name, signature=signature)
    else:
        wrapper = JavaField(java_class=java_class, name=name, signature=signature)
    return wrapper


@public
@annotate(java_class=JavaClass, static=bool)
def _cache_methods(java_class, name, static):

    jclass = JVM.jvm.JClass(None, java_class.__javaclass__, borrowed=True)

    jclass_hash = jclass.hashCode()

    methods_map = (_static_methods_cache if static else _instance_methods_cache).get(jclass_hash) # {str: {Method}}
    if methods_map is None:
        try:
            java_methods = jclass.getMethods()
        except:
            return None

        static_methods_map   = {} # {str: {Method}}
        instance_methods_map = {} # {str: {Method}}

        for java_method in java_methods:
            modifiers = java_method.getModifiers()
            is_public = EJavaModifiers.PUBLIC in modifiers
            is_static = EJavaModifiers.STATIC in modifiers
            if is_public:
                method_name = str(java_method.getName())
                alternatives_map = static_methods_map if is_static else instance_methods_map
                alternatives = alternatives_map.get(method_name) # {Method}
                if alternatives is None:
                    alternatives_map[method_name] = alternatives = set()
                alternatives.add(java_method)

        _static_methods_cache[jclass_hash]   = static_methods_map
        _instance_methods_cache[jclass_hash] = instance_methods_map

        methods_map = static_methods_map if static else instance_methods_map

    java_methods = methods_map.get(name)
    if not java_methods:
        return None

    if static:
        wrapper = StaticJavaMethod(java_class=java_class, name=name)
    else:
        wrapper = JavaMethod(java_class=java_class, name=name)

    for java_method in java_methods:
        params_java_types = java_method.getParameterTypes()
        return_java_type  = java_method.getReturnType()
        wrapper.add(_signature_for_params(params_java_types),
                    _signature_for_type(return_java_type))

    return wrapper


# A cache of known JavaClass instances. This is requried so that when
# we do a return_cast() to a return type, we don't have to recreate
# the class every time - we can re-use the existing class.
_class_cache = {}

# A 2 level maps of Class:
#
# Method name: Method for static methods
_static_methods_cache   = {} # {Class, {str: {Method}}}
# Method name: Method for instance methods
_instance_methods_cache = {} # {Class, {str: {Method}}}
