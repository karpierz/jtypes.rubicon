# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from ._jclass import _cache_field, _cache_methods


@public
class JavaInstance(object):

    def __init__(self, *args, **kwargs):

        jobject = kwargs.pop("jni", None)

        if kwargs:
            raise ValueError("Can't construct instance of {} using keyword arguments.".format(
                             self.__class__))

        if jobject is None:

            klass = self.__class__.__javaclass__

            ##################################################################
            # Check that we know the constructors for the class
            ##################################################################

            class_dict = self.__class__.__dict__

            constructors = class_dict["_constructors"]
            if constructors is None:
                constructors = {}
                with JFrame(jenv, 1): # constructors_j
                    constructors_j = java.CallObjectMethod(class_dict["__javaclass__"], reflect.Class__getConstructors)
                    if constructors_j.value is None:
                        raise RuntimeError("Couldn't get constructor for '{}'".format(self))
                    constructors_j = cast(constructors_j, jobjectArray)

                    for i in range(java.GetArrayLength(constructors_j)):
                        with JFrame(jenv, 2): # constructor, params
                            constructor = java.GetObjectArrayElement(constructors_j, i)

                            modifiers = java.CallIntMethod(constructor, reflect.Constructor__getModifiers)
                            is_public = java.CallStaticBooleanMethod(reflect.Modifier, reflect.Modifier__isPublic, modifiers)
                            if is_public:
                                # We now know that a constructor exists, and we know the signature
                                # of those constructors. However, we won't resolve the method
                                # implementing the constructor until we need it.
                                params = java.CallObjectMethod(constructor, reflect.Constructor__getParameterTypes)
                                params = cast(params, jobjectArray)
                                constructors[signature_for_params(params)] = None

                    type.__setattr__(self.__class__, "_constructors", constructors)

            ##################################################################
            # Invoke the JNI constructor
            ##################################################################
            try:
                arg_sig, match_types, constructor = select_polymorph(constructors, args)
                if constructor is None:
                    sig = "".join(match_types)
                    constructor = java.GetMethodID(klass, "<init>", "({})V".format("".join(sig)))
                    if constructor is None:
                        raise RuntimeError("Couldn't get method ID for {} constructor of {}".format(
                                           sig, self.__class__))
                    class_dict["_constructors"][sig] = constructor

                jobject = java.NewObject(klass, constructor, *convert_args(args, match_types))
                if not jobject:
                    raise RuntimeError("Couldn't instantiate Java instance of {}.".format(
                                       self.__class__))
                jobject = cast(java.NewGlobalRef(jobject), jclass)
                if jobject.value is None:
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

    def __repr__(self):

        return "<{}: {}>".format(self.__class__.__name__, self.__javaobject__.value)

    def __str__(self):

        return self.toString()

    def __unicode__(self):

        return self.toString()

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
