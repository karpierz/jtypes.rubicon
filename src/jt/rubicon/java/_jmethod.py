# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from ._conversion import return_cast


@public
class StaticJavaMethod(object):

    """The representation for a static method on a Java object

    Constructor requires:
     * java_class - the Python representation of the Java class
     * name - the method name being invoked.
    """
    def __init__(self, java_class, name):

        self.java_class  = java_class
        self.name        = name
        self._polymorphs = {}

    def add(self, params_signature, return_signature):

        if params_signature not in self._polymorphs:

            invoker = {
                "V": java.CallStaticVoidMethod,
                "Z": java.CallStaticBooleanMethod,
                "C": java.CallStaticCharMethod,
                "B": java.CallStaticByteMethod,
                "S": java.CallStaticShortMethod,
                "I": java.CallStaticIntMethod,
                "J": java.CallStaticLongMethod,
                "F": java.CallStaticFloatMethod,
                "D": java.CallStaticDoubleMethod,
            }.get(return_signature, java.CallStaticObjectMethod)

            class_dict = self.java_class.__dict__
            jclass = class_dict["__javaclass__"]

            full_signature = "({}){}".format(params_signature, return_signature)
            jmethod_id = java.GetStaticMethodID(jclass, self.name, full_signature)
            if jmethod_id.value is None:
                raise RuntimeError("Couldn't find static Java method '{}.{}' with signature "
                                   "'{}'".format(class_dict["_descriptor"],
                                                 self.name, full_signature))

            self._polymorphs[params_signature] = dict(return_signature=return_signature,
                                                      invoker=invoker,
                                                      jmethod_id=jmethod_id)

    def __call__(self, *args):

        class_dict = self.java_class.__dict__

        try:
            jclass = class_dict["__javaclass__"]
            arg_sig, match_types, polymorph = select_polymorph(self._polymorphs, args)
            result = polymorph["invoker"](jclass,
                                          polymorph["jmethod_id"],
                                          *convert_args(args, match_types))
            return return_cast(result, polymorph["return_signature"])
        except KeyError as exc:
            raise ValueError("Can't find Java static method '{}.{}' matching argument signature "
                             "'{}'. Options are: {}".format(class_dict["_descriptor"],
                                                            self.name, exc, self._polymorphs.keys()))

@public
class JavaMethod(object):

    def __init__(self, java_class, name):

        self.java_class  = java_class
        self.name        = name
        self._polymorphs = {}

    def add(self, params_signature, return_signature):

        invoker = {
            "V": java.CallVoidMethod,
            "Z": java.CallBooleanMethod,
            "C": java.CallCharMethod,
            "B": java.CallByteMethod,
            "S": java.CallShortMethod,
            "I": java.CallIntMethod,
            "J": java.CallLongMethod,
            "F": java.CallFloatMethod,
            "D": java.CallDoubleMethod,
        }.get(return_signature, java.CallObjectMethod)

        class_dict = self.java_class.__dict__
        jclass = class_dict["__javaclass__"]

        full_signature = "({}){}".format(params_signature, return_signature)
        jmethod_id = java.GetMethodID(jclass, self.name, full_signature)
        if jmethod_id.value is None:
            raise RuntimeError("Couldn't find Java method '{}.{}' with signature "
                               "'{}'".format(class_dict["_descriptor"],
                                             self.name, full_signature))

        self._polymorphs[params_signature] = dict(return_signature=return_signature,
                                                  invoker=invoker,
                                                  jmethod_id=jmethod_id)

    def __call__(self, instance, *args):

        class_dict = self.java_class.__dict__

        try:
            arg_sig, match_types, polymorph = select_polymorph(self._polymorphs, args)
            result = polymorph["invoker"](instance,
                                          polymorph["jmethod_id"],
                                          *convert_args(args, match_types))
            return return_cast(result, polymorph["return_signature"])
        except KeyError as exc:
            raise ValueError("Can't find Java instance method '{}.{}' matching argument signature "
                             "'{}'. Options are: {}".format(class_dict["_descriptor"],
                                                            self.name, exc, self._polymorphs.keys()))


@public
class BoundJavaMethod(object):

    def __init__(self, instance, method):

        self.instance = instance
        self.method   = method

    def __call__(self, *args):

        return self.method(self.instance, *args)
