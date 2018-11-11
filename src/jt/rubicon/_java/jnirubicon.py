# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib.compat import *
from ...jvm.lib import annotate
from ...        import jni

from ...jvm.java.jnij import jnij
from ...jvm.java      import registerClass
from ...jvm.java      import registerNatives
from ...jvm.java      import unregisterNatives


class rubicon_reflect_ProxyHandler(jnij):

    @annotate(jenv=jni.JNIEnv)
    def initialize(self, jenv):

        from .org.pybee.rubicon.reflect import ProxyHandler
        unregisterNatives(jenv, "com.jt.reflect.ProxyHandler")
        registerNatives(jenv,   "com.jt.reflect.ProxyHandler", ProxyHandler)

class rubicon_Python(jnij):

    @annotate(jenv=jni.JNIEnv)
    def initialize(self, jenv):

        from .org.pybee.rubicon import Python
        registerClass(jenv, "org.pybee.rubicon.Python", Python)
