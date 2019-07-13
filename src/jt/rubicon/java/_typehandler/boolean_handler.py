# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public

from .._constants import EJavaType
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler


@public
class BooleanHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(BooleanHandler, self).__init__(state, EJavaType.BOOLEAN, "Z")

    def match(self, val):

        if isinstance(val, bool):
            return EMatchType.PERFECT
        return EMatchType.NONE

    def toJava(self, val):

        return self._jt_jvm.JObject.newBoolean(bool(val))

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.booleanValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticBooleanField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticBooleanField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetBooleanField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetBooleanField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        args.setBoolean(pos, bool(val))

    """
    elif arg_definition == "C":

        args.setChar(pos, val)
    """

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticBooleanMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallBooleanMethod(this, meth, args.arguments)
