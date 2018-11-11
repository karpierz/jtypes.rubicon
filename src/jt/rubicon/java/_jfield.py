# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import annotate
from ...jvm.lib import public

from ._conversion import return_cast


@public
class StaticJavaField(object):

    def __init__(self, java_class, name, signature):

        self.java_class = java_class
        self.name       = name
        self._signature = signature

        self._accessor = {
            "Z": java.GetStaticBooleanField,
            "B": java.GetStaticByteField,
            "C": java.GetStaticCharField,
            "S": java.GetStaticShortField,
            "I": java.GetStaticIntField,
            "J": java.GetStaticLongField,
            "F": java.GetStaticFloatField,
            "D": java.GetStaticDoubleField,
        }.get(self._signature, java.GetStaticObjectField)

        self._mutator = {
            "Z": java.SetStaticBooleanField,
            "B": java.SetStaticByteField,
            "C": java.SetStaticCharField,
            "S": java.SetStaticShortField,
            "I": java.SetStaticIntField,
            "J": java.SetStaticLongField,
            "F": java.SetStaticFloatField,
            "D": java.SetStaticDoubleField,
        }.get(self._signature, java.SetStaticObjectField)

        class_dict = self.java_class.__dict__
        jclass = class_dict["__javaclass__"]

        self.__jfield_id = java.GetStaticFieldID(jclass, self.name, self._signature)
        if self.__jfield_id.value is None:
            raise RuntimeError("Couldn't find static Java field '{}.{}'".format(
                               jclass, self.name))

    def get(self):

        class_dict = self.java_class.__dict__
        jclass = class_dict["__javaclass__"]

        result = self._accessor(jclass, self.__jfield_id)
        return return_cast(result, self._signature)

    def set(self, value):

        class_dict = self.java_class.__dict__
        jclass = class_dict["__javaclass__"]

        self._mutator(jclass, self.__jfield_id, value)


@public
class JavaField(object):

    def __init__(self, java_class, name, signature):

        self.java_class = java_class
        self.name       = name
        self._signature = signature

        self._accessor = {
            "Z": java.GetBooleanField,
            "B": java.GetByteField,
            "C": java.GetCharField,
            "S": java.GetShortField,
            "I": java.GetIntField,
            "J": java.GetLongField,
            "F": java.GetFloatField,
            "D": java.GetDoubleField,
        }.get(self._signature, java.GetObjectField)

        self._mutator = {
            "Z": java.SetBooleanField,
            "B": java.SetByteField,
            "C": java.SetCharField,
            "S": java.SetShortField,
            "I": java.SetIntField,
            "J": java.SetLongField,
            "F": java.SetFloatField,
            "D": java.SetDoubleField,
        }.get(self._signature, java.SetObjectField)

        class_dict = self.java_class.__dict__
        jclass = class_dict["__javaclass__"]

        self.__jfield_id = java.GetFieldID(jclass, self.name, self._signature)
        if self.__jfield_id.value is None:
            raise RuntimeError("Couldn't find Java field '{}.{}'".format(
                               jclass, self.name))

    def get(self, instance):

        this = instance.__javaobject__

        result = self._accessor(this, self.__jfield_id)
        return return_cast(result, self._signature)

    def set(self, instance, value):

        this = instance.__javaobject__

        self._mutator(this, self.__jfield_id, value)
