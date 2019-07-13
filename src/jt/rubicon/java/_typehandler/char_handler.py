# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import

import collections as abcoll

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public

from .._constants import EJavaType
from .._jvm       import JVM

from ._base_handler import _PrimitiveHandler
from ._base_handler import str_types


@public
class CharHandler(_PrimitiveHandler):

    __slots__ = ()

    def __init__(self, state):

        super(CharHandler, self).__init__(state, EJavaType.CHAR, "C")

    def match(self, val):

        if isinstance(val, str_types):
            if len(val) == 1:
                return EMatchType.PERFECT
        return EMatchType.NONE

    def valid(self, val):

        if isinstance(val, str_types):
            if len(val) != 1:
                return False
        return True

    def toJava(self, val):

        return self._jt_jvm.JObject.newCharacter(val) #!!! ??? chr(val) !!!

    def toPython(self, val):

        if isinstance(val, self._jt_jvm.JObject):
            return val.charValue()
        else:
            return val

    def getStatic(self, fld, cls):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetStaticCharField(cls, fld)

    def setStatic(self, fld, cls, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetStaticCharField(cls, fld, val)

    def getInstance(self, fld, this):

        with JVM.jvm as (jvm, jenv):
            return jenv.GetCharField(this, fld)

    def setInstance(self, fld, this, val):

        with JVM.jvm as (jvm, jenv):
            jenv.SetCharField(this, fld, val)

    def setArgument(self, pdescr, args, pos, val):

        if isinstance(val, str):
            args.setChar(pos, val)
        elif isinstance(val, str_types):
            # never reached for PY>=3
            args.setChar(pos, val.decode())
        else:
            args.setChar(pos, str(val))

    def callStatic(self, meth, cls, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallStaticCharMethod(cls, meth, args.arguments)

    def callInstance(self, meth, this, args):

        with JVM.jvm as (jvm, jenv):
            return jenv.CallCharMethod(this, meth, args.arguments)
