# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public

from ....jvm.jtypehandlerabc import TypeHandlerABC

from .._constants import EJavaType
from .._jvm       import JVM

int_types  = (int, long)
num_types  = (float, int, long)
str_types  = (builtins.str, str)
byte_types = (bytes, bytearray)


class _BaseHandler(TypeHandlerABC):

    __slots__ = ()

    _jt_jvm = property(lambda self: JVM.jvm)

    def isSubtypeOf(self, other):

        raise NotImplementedError()

    def newArray(self, size):

        raise NotImplementedError()

    def getElement(self, arr, idx):

        raise NotImplementedError()

    def setElement(self, arr, idx, val):

        raise NotImplementedError()

    def getSlice(self, arr, start, stop, step):

        raise NotImplementedError()

    def setSlice(self, arr, start, stop, step, val):

        raise NotImplementedError()

    def getArrayBuffer(self, arr):

        raise NotImplementedError()

    def releaseArrayBuffer(self, arr, buf):

        raise NotImplementedError()


class _PrimitiveHandler(_BaseHandler):

    __slots__ = ()

    def valid(self, val):

        return True


class _ObjectHandler(_BaseHandler):

    __slots__ = ()

    def valid(self, val):

        return True

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            result = jenv.GetStaticObjectField(cls, fld)
            return self.toPython(result)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticObjectField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            result = jenv.GetObjectField(this, fld)
            return self.toPython(result)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetObjectField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setObject(pos, self.toJava(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            result = jenv.CallStaticObjectMethod(cls, meth, args.arguments)
            return self.toPython(result)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            result = jenv.CallObjectMethod(this, meth, args.arguments)
            return self.toPython(result)
