# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from .            import types as jtypes
from ._jproxy     import JavaProxy
from ._exceptions import UnknownClassException


@public
class JavaClass(type):

    def __new__(cls, descriptor):

        try:
            return _class_cache[descriptor]
        except KeyError:
            jclass = java.FindClass(descriptor)
            if jclass.value is None:
                raise UnknownClassException(descriptor)
            jclass = cast(java.NewGlobalRef(jclass), jtypes.jclass)
            if jclass.value is None:
                raise RuntimeError("Unable to create global reference to class.")

            ##################################################################
            # Determine the alternate types for this class
            ##################################################################

            # Best option is the type itself
            alternates = ["L{};".format(descriptor)]

            # Next preference is an interfaces
            with JFrame(jenv, 1): # java_interfaces
                java_interfaces = java.CallObjectMethod(jclass, reflect.Class__getInterfaces)
                if java_interfaces.value is None:
                    raise RuntimeError("Couldn't get interfaces for '{}'".format(self))
                java_interfaces = cast(java_interfaces, jobjectArray)

                for i in range(java.GetArrayLength(java_interfaces)):
                    with JFrame(jenv, 2): # java_interface, name
                        java_interface = java.GetObjectArrayElement(java_interfaces, i)

                        name = java.CallObjectMethod(java_interface, reflect.Class__getName)
                        name_str = java.GetStringUTFChars(cast(name, jtypes.jstring), None)

                        alternates.append("L{};".format(name_str.replace('.', '/')))

            # Then check all the superclasses
            java_superclass = jclass
            while True:
                with JFrame(jenv, 2): # java_superclass, name
                    java_superclass = java.CallObjectMethod(java_superclass, reflect.Class__getSuperclass)
                    if java_superclass.value is None:
                        break

                    name = java.CallObjectMethod(java_superclass, reflect.Class__getName)
                    name_str = java.GetStringUTFChars(cast(name, jtypes.jstring), None)

                    alternates.append("L{};".format(name_str.replace('.', '/')))

            # Cache the class instance, so we don't have to recreate it
            bases = (JavaInstance,)
            name  = descriptor.encode("utf-8")
            attrs = dict(_descriptor=descriptor,
                         __javaclass__=jclass,
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
                                                                          name, bases, attrs)
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
            descriptor, = args
            name  = descriptor.encode("utf-8")
            bases = (JavaProxy,)
            attrs = {}
        else:
            name, bases, attrs = args
            descriptor = bases[-1].__dict__["_descriptor"]
        attrs.update(_descriptor=descriptor,
                     _alternates=["L{};".format(descriptor)],
                     _methods={})
        java_class = super(JavaInterface, cls).__new__(cls, name, bases, attrs)

        jclass = java.FindClass(descriptor)
        if jclass is None:
            raise UnknownClassException(descriptor)
        java_class.__javaclass__ = cast(java.NewGlobalRef(jclass), jtypes.jclass)
        if java_class.__javaclass__.value is None:
            raise RuntimeError("Unable to create global reference to interface.")

        ##################################################################
        # Load the methods for the class
        ##################################################################
        methods = java.CallObjectMethod(jclass, reflect.Class__getMethods)
        if methods is None:
            raise RuntimeError("Couldn't get methods for '{}'".format(self))
        methods = cast(methods, jobjectArray)

        method_count = java.GetArrayLength(methods)
        for i in range(method_count):
            java_method = java.GetObjectArrayElement(methods, i)
            modifiers = java.CallIntMethod(java_method, reflect.Method__getModifiers)

            public = java.CallStaticBooleanMethod(reflect.Modifier, reflect.Modifier__isPublic, modifiers)
            if public:
                static = java.CallStaticBooleanMethod(reflect.Modifier, reflect.Modifier__isStatic, modifiers)
                if not static:
                    name = java.CallObjectMethod(java_method, reflect.Method__getName)
                    name_str = java.GetStringUTFChars(cast(name, jtypes.jstring), None)

                    params = java.CallObjectMethod(java_method, reflect.Method__getParameterTypes)
                    params = cast(params, jobjectArray)

                    java_class._methods.setdefault(name_str, set()).add(type_names_for_params(params))

        return java_class

    def __repr__(self):

        return "<JavaInterface: {}>".format(self._descriptor)


@public
@anotate(java_class=JavaClass, static=bool)
def _cache_field(java_class, name, static):

    class_dict = java_class.__dict__
    jclass = class_dict["__javaclass__"]

    with JFrame(jenv, 3): # java_field, java_type, type_name

        java_field = java.CallStaticObjectMethod(reflect.Python, reflect.Python__getField,
                                                 jclass,
                                                 java.NewStringUTF(name), jboolean(static))
        if not java_field.value:
            return None

        java_type = java.CallObjectMethod(java_field, reflect.Field__getType)

        type_name = java.CallObjectMethod(java_type,  reflect.Class__getName)
        field_type_name = java.GetStringUTFChars(cast(type_name, jtypes.jstring), None)

        if static:
            wrapper = StaticJavaField(java_class=java_class, name=name,
                                      signature=signature_for_type_name(field_type_name))
        else:
            wrapper = JavaField(java_class=java_class, name=name,
                                signature=signature_for_type_name(field_type_name))

    return wrapper


@public
@anotate(java_class=JavaClass, static=bool)
def _cache_methods(java_class, name, static):

    class_dict = java_class.__dict__
    jclass = class_dict["__javaclass__"]

    with JFrame(jenv, 1): # java_methods
        java_methods = java.CallStaticObjectMethod(reflect.Python, reflect.Python__getMethods,
                                                   jclass,
                                                   java.NewStringUTF(name), jboolean(static))
        if not java_methods.value:
            return None
        java_methods = cast(java_methods, jobjectArray)

        if static:
            wrapper = StaticJavaMethod(java_class=java_class, name=name)
        else:
            wrapper = JavaMethod(java_class=java_class, name=name)

        for i in range(java.GetArrayLength(java_methods)):
            with JFrame(jenv, 4): # java_method, params, java_type, type_name
                java_method = java.GetObjectArrayElement(java_methods, i)

                params = java.CallObjectMethod(java_method, reflect.Method__getParameterTypes)
                params = cast(params, jobjectArray)

                java_type = java.CallObjectMethod(java_method, reflect.Method__getReturnType)

                type_name = java.CallObjectMethod(java_type, reflect.Class__getName)
                return_type_name = java.GetStringUTFChars(cast(type_name, jtypes.jstring), None)

                wrapper.add(signature_for_params(params), signature_for_type_name(return_type_name))

    return wrapper


# A cache of known JavaClass instances. This is requried so that when
# we do a return_cast() to a return type, we don't have to recreate
# the class every time - we can re-use the existing class.
_class_cache = {}
