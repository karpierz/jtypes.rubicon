# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import py2compatible
from ...jvm.lib import annotate
from ...jvm.lib import public
from ...jvm.jframe import JFrame

from ._constants  import EJavaModifiers
from ._jvm        import JVM
from ._jmethod    import BoundJavaMethod
from ._conversion import _convert_args_to_jargs, select_polymorph, _signature_for_params
from ._jclass     import _cache_field, _cache_methods
from .            import types as jtypes


@public
@py2compatible
class JavaInstance(object):

    def __init__(self, *args, **kwargs):

        jobject = kwargs.pop("jni", None)

        if kwargs:
            raise ValueError("Can't construct instance of {} using keyword arguments.".format(
                             self.__class__))

        if jobject is None:

            jclass = JVM.jvm.JClass(None, self.__class__.__javaclass__, borrowed=True)

            # Check that we know the constructors for the class

            class_dict = self.__class__.__dict__

            constructors = class_dict["_constructors"]
            if constructors is None:

                constructors = {}

                try:
                    jconstructors = jclass.getConstructors()
                except:
                    raise RuntimeError("Couldn't get constructor for '{}'".format(self))
                for jconstructor in jconstructors:
                    modifiers = jconstructor.getModifiers()
                    is_public = EJavaModifiers.PUBLIC in modifiers
                    if is_public:
                        # We now know that a constructor exists, and we know the signature
                        # of those constructors. However, we won't resolve the method
                        # implementing the constructor until we need it.
                        ctor_params = jconstructor.getParameterTypes()
                        constructors[_signature_for_params(ctor_params)] = None

                type.__setattr__(self.__class__, "_constructors", constructors)

            # Invoke the JNI constructor

            try:
                arg_sig, match_types, constructor = select_polymorph(constructors, args)
                if constructor is None:
                    sig = "".join(match_types)
                    with JVM.jvm as (jvm, jenv):
                        try:
                            constructor = jenv.GetMethodID(jclass.handle, b"<init>", "({})V".format("".join(sig)).encode("utf-8"))
                        except: # <AK> was: if constructor is None:
                            raise RuntimeError("Couldn't get method ID for {} constructor of {}".format(
                                               sig, self.__class__))
                    class_dict["_constructors"][sig] = constructor

                with JVM.jvm as (jvm, jenv), JFrame(jenv, 1):
                    try:
                        jargs = _convert_args_to_jargs(args, match_types)
                        jobject = jenv.NewObject(jclass.handle, constructor, jargs.arguments)
                    except: # <AK> was: if not jobject:
                        raise RuntimeError("Couldn't instantiate Java instance of {}.".format(
                                           self.__class__))
                    try:
                        jobject = jtypes.cast(jenv.NewGlobalRef(jobject), jtypes.jclass)
                    except: # <AK> was: if jobject.value is None:
                        raise RuntimeError("Unable to create global reference to instance.")

            except KeyError as exc:
                raise ValueError("Can't find constructor matching argument signature {}. "
                                 "Options are: {}".format(exc, ", ".join(constructors.keys())))

        # This is just:
        #    self.__javaobject__ = jobject
        #    self._as_parameter_ = jobject
        # but we can't make that call, because we've overridden __setattr__
        # to only respond to Java fields.
        object.__setattr__(self, "__javaobject__", jobject)
        object.__setattr__(self, "_as_parameter_", jobject)

    def __str__(self):

        return self.toString()

    def __repr__(self):

        return "<{}: {}>".format(self.__class__.__name__, self.__javaobject__.value)

    def __getattr__(self, name):

        class_dict = self.__class__.__dict__

        # First try to find a field match
        try:
            field_wrapper = class_dict["_members"]["fields"][name]
        except KeyError:
            field_wrapper = class_dict["_members"]["fields"][name] = _cache_field(self.__class__, name, False)

        if field_wrapper:
            return field_wrapper.get(self)

        # Then try to find a method match
        try:
            method_wrapper = class_dict["_members"]["methods"][name]
        except KeyError:
            method_wrapper = class_dict["_members"]["methods"][name] = _cache_methods(self.__class__, name, False)

        if method_wrapper:
            return BoundJavaMethod(self, method_wrapper)

        raise AttributeError("'{}' Java object has no attribute '{}'".format(
                             self.__class__.__name__, name))

    def __setattr__(self, name, value):

        class_dict = self.__class__.__dict__

        # Try to find a field match.
        try:
            field_wrapper = class_dict["_members"]["fields"][name]
        except KeyError:
            field_wrapper = class_dict["_members"]["fields"][name] = _cache_field(self.__class__, name, False)

        if field_wrapper:
            return field_wrapper.set(self, value)

        raise AttributeError("'{}' Java object has no attribute '{}'".format(
                             self.__class__.__name__, name))
