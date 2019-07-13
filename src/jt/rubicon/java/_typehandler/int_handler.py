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
class IntHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(IntHandler, self).__init__(state, EJavaType.INT, "I")

    def match(self, val):

        if isinstance(val, int) or (isinstance(val, long) and val <= 2147483647):
            return EMatchType.PERFECT
        elif isinstance(val, float):
            return EMatchType.IMPLICIT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, int_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxIntValue()
            if not (min_val <= val <= max_val):
                return False
        return True

    def toJava(self, val):

        return self._jt_jvm.JObject.newInteger(val)

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.intValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticIntField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticIntField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetIntField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetIntField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setInt(pos, int(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticIntMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallIntMethod(this, meth, args.arguments)
