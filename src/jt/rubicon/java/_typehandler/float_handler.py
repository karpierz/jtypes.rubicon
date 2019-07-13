# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public

from .._constants import EJavaType
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler
from ._base_handler import num_types


@public
class FloatHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(FloatHandler, self).__init__(state, EJavaType.FLOAT, "F")

    def match(self, val):

        if isinstance(val, float):
            return EMatchType.PERFECT
        elif isinstance(val, int):
            return EMatchType.IMPLICIT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, num_types):
            min_val, max_val = self._jt_jvm.JObject.minmaxFloatValue()
            if ((val > 0.0 and not ( min_val <= val <=  max_val)) or
                (val < 0.0 and not (-max_val <= val <= -min_val))):
                return False
        return True

    def toJava(self, val):

        return self._jt_jvm.JObject.newFloat(val)

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.floatValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticFloatField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticFloatField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetFloatField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetFloatField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setFloat(pos, float(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticFloatMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallFloatMethod(this, meth, args.arguments)
