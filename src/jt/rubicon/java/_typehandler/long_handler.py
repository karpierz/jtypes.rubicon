# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public

from .._constants import EJavaType
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler
from ._base_handler import int_types


@public
class LongHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(LongHandler, self).__init__(state, EJavaType.LONG, "J")

    def match(self, val):

        if isinstance(val, (int, long)):
            return EMatchType.PERFECT
        elif isinstance(val, float):
            return EMatchType.IMPLICIT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, int_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxLongValue()
            if not (min_val <= val <= max_val):
                return False
        return True

    def toJava(self, val):

        return self._jt_jvm.JObject.newLong(val)

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.longValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticLongField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticLongField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetLongField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetLongField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setLong(pos, long(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticLongMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallLongMethod(this, meth, args.arguments)
