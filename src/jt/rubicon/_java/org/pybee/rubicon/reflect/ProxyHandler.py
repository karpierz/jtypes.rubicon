# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import

import traceback

from .......           import jni
from .......jvm.jframe import JFrame
from .......jvm.jhost  import JHost
from .......jvm.java   import throwJavaException

from ......java._jvm    import JVM
from ......java._jproxy import dispatch


# Class: com.jt.reflect.ProxyHandler

# Method: native Object invoke(long target, Object proxy, java.lang.reflect.Method method, Object[] args);

@jni.method("(JLjava/lang/Object;Ljava/lang/reflect/Method;[Ljava/lang/Object;)Ljava/lang/Object;")
def invoke(env, this,
           target, jproxy, jmethod, jargs):

    # Implementation of the InvocationHandler used by all Python objects.
    #
    # This method converts the Python method invocation into a call on the
    # method dispatch method that has been registered as part of the runtime.

    jt_jvm = JVM.jvm
    jenv = env[0]
    try:
        with JHost.CallbackState():
            method, args = None, []
            try:
                instance = jni.from_oid(target)

                method = jt_jvm.JMethod(None, jmethod, own=False) if jmethod else None
                method_name = method.getName()

                argcnt = jenv.GetArrayLength(jargs) if jargs else 0
                with JFrame(jenv, argcnt):
                    for idx in range(argcnt):
                        jarg = jenv.GetObjectArrayElement(jargs, idx)
                        args.append(jarg) # (unsigned long)jarg
                    args = tuple(args)

                    result = dispatch(id(instance), method_name, args)

                    if result is None:
                        return None
                    else:
                        return # ???
            finally:
                del method, args
    except Exception as exc:
        #if result == NULL:
        traceback.print_exc()

    return None

# Method: native void initialize(long target);

@jni.method("(J)V")
def initialize(env, this,
               target):
    pass

# Method: native void release(long target);

@jni.method("(J)V")
def release(env, this,
            target):
    pass


__jnimethods__ = (
    invoke,
    initialize,
    release,
)
