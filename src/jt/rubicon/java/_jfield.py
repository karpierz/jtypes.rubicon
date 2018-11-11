# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from ._jvm import JVM


@public
class StaticJavaField(object):

    # Equivalent of: jt.jtypes.JavaField

    def __init__(self, java_class, name, signature):

        self.java_class  = java_class
        self.name        = name
        self.__signature = signature
        type_manager = JVM.jvm.type_manager
        self.__thandler  = type_manager.get_handler(self.__signature)

        with JVM.jvm as (jvm, jenv):
            try:
                self.__jfield_id = jenv.GetStaticFieldID(self.java_class.__javaclass__,
                                                         self.name.encode("utf-8"),
                                                         self.__signature.encode("utf-8"))
            except: # <AK> was: if self.__jfield_id.value is None:
                raise RuntimeError("Couldn't find static Java field '{}.{}'".format(
                                   self.java_class.__javaclass__, self.name))

    def get(self):

        return self.__thandler.getStatic(self.__jfield_id, self.java_class.__javaclass__)

    def set(self, value):

        from ..__config__ import config

        if config.getboolean("WITH_VALID", False) and not self.__thandler.valid(value):
            raise ValueError("Assigned value is not valid for required field type.")

        self.__thandler.setStatic(self.__jfield_id, self.java_class.__javaclass__, value)


@public
class JavaField(object):

    # Equivalent of: jt.jtypes.JavaField

    def __init__(self, java_class, name, signature):

        self.java_class  = java_class
        self.name        = name
        self.__signature = signature
        type_manager = JVM.jvm.type_manager
        self.__thandler  = type_manager.get_handler(self.__signature)

        with JVM.jvm as (jvm, jenv):
            try:
                self.__jfield_id = jenv.GetFieldID(self.java_class.__javaclass__,
                                                   self.name.encode("utf-8"),
                                                   self.__signature.encode("utf-8"))
            except: # <AK> was: if self.__jfield_id.value is None:
                raise RuntimeError("Couldn't find Java field '{}.{}'".format(
                                   self.java_class.__javaclass__, self.name))

    def get(self, instance):

        return self.__thandler.getInstance(self.__jfield_id, instance.__javaobject__)

    def set(self, instance, value):

        from ..__config__ import config

        if config.getboolean("WITH_VALID", False) and not self.__thandler.valid(value):
            raise ValueError("Assigned value is not valid for required field type.")

        self.__thandler.setInstance(self.__jfield_id, instance.__javaobject__, value)
