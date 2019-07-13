# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public
from ....jvm.lib import issequence

from .._constants import EJavaType
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler
from ._base_handler import int_types, byte_types


@public
class ByteHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(ByteHandler, self).__init__(state, EJavaType.BYTE, "B")

    def match(self, val):

        if isinstance(val, int):
            return EMatchType.PERFECT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, int_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxByteValue()
            if not (min_val <= val <= max_val):
                return False
        return True

    def toJava(self, val):

        return self._jt_jvm.JObject.newByte(val)

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.byteValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticByteField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticByteField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetByteField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetByteField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setByte(pos, int(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticByteMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallByteMethod(this, meth, args.arguments)
