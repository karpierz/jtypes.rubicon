# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from ._jvm        import JVM
from ._conversion import _convert_args_to_jargs, select_polymorph


@public
class StaticJavaMethod(object):

    """The representation for a static method on a Java object

    Constructor requires:
     * java_class - the Python representation of the Java class
     * name       - the method name being invoked.
    """
    def __init__(self, java_class, name):

        self.java_class   = java_class
        self.name         = name
        self.__polymorphs = {}

    def add(self, params_signature, return_signature):

        if params_signature in self.__polymorphs:
            return

        type_manager = JVM.jvm.type_manager
        thandler = type_manager.get_handler(return_signature)
	
        full_signature = "({}){}".format(params_signature, return_signature)

        with JVM.jvm as (jvm, jenv):
            try:
                jmethod_id = jenv.GetStaticMethodID(self.java_class.__javaclass__,
                                                    self.name.encode("utf-8"),
                                                    full_signature.encode("utf-8"))
            except: # <AK> was: if jmethod_id.value is None:
                raise RuntimeError("Couldn't find static Java method '{}.{}' with signature "
                                   "'{}'".format(self.java_class.__dict__["_descriptor"],
                                                 self.name, full_signature))

        self.__polymorphs[params_signature] = dict(thandler=thandler,
                                                   jmethod_id=jmethod_id)

    def __call__(self, *args):

        try:
            arg_sig, match_types, polymorph = select_polymorph(self.__polymorphs, args)
            jmethod_id = polymorph["jmethod_id"]
            jargs = _convert_args_to_jargs(args, match_types)
            thandler = polymorph["thandler"]
            return thandler.callStatic(jmethod_id, self.java_class.__javaclass__, jargs)
        except KeyError as exc:
            raise ValueError("Can't find Java static method '{}.{}' matching argument signature "
                             "'{}'. Options are: {}".format(self.java_class.__dict__["_descriptor"],
                                                            self.name, exc, self.__polymorphs.keys()))

@public
class JavaMethod(object):

    def __init__(self, java_class, name):

        self.java_class   = java_class
        self.name         = name
        self.__polymorphs = {}

    def add(self, params_signature, return_signature):

        type_manager = JVM.jvm.type_manager
        thandler = type_manager.get_handler(return_signature)

        full_signature = "({}){}".format(params_signature, return_signature)

        with JVM.jvm as (jvm, jenv):
            try:
                jmethod_id = jenv.GetMethodID(self.java_class.__javaclass__,
                                              self.name.encode("utf-8"),
                                              full_signature.encode("utf-8"))
            except: # <AK> was: if jmethod_id.value is None:
                raise RuntimeError("Couldn't find Java method '{}.{}' with signature "
                                   "'{}'".format(self.java_class.__dict__["_descriptor"],
                                                 self.name, full_signature))

        self.__polymorphs[params_signature] = dict(thandler=thandler,
                                                   jmethod_id=jmethod_id)

    def __call__(self, instance, *args):

        try:
            arg_sig, match_types, polymorph = select_polymorph(self.__polymorphs, args)
            jmethod_id = polymorph["jmethod_id"]
            jargs = _convert_args_to_jargs(args, match_types)
            thandler = polymorph["thandler"]
            return thandler.callInstance(jmethod_id, instance, jargs)
        except KeyError as exc:
            raise ValueError("Can't find Java instance method '{}.{}' matching argument signature "
                             "'{}'. Options are: {}".format(self.java_class.__dict__["_descriptor"],
                                                            self.name, exc, self.__polymorphs.keys()))


@public
class BoundJavaMethod(object):

    def __init__(self, instance, method):

        self.instance = instance
        self.method   = method

    def __call__(self, *args):

        return self.method(self.instance, *args)
