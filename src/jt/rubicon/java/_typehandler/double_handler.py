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
class DoubleHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(DoubleHandler, self).__init__(state, EJavaType.DOUBLE, "D")

    def match(self, val):

        if isinstance(val, float):
            return EMatchType.PERFECT
        elif isinstance(val, int):
            return EMatchType.IMPLICIT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, int_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxDoubleValue()
            if ((val > 0.0 and not ( min_val <= val <=  max_val)) or
                (val < 0.0 and not (-max_val <= val <= -min_val))):
                return False
        return True

    def toJava(self, val):

        return self._jt_jvm.JObject.newDouble(val)

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.doubleValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticDoubleField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticDoubleField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetDoubleField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetDoubleField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setDouble(pos, float(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticDoubleMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallDoubleMethod(this, meth, args.arguments)
