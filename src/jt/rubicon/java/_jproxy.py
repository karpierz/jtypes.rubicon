# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import

import traceback

from ...jvm.lib import annotate
from ...jvm.lib import public
from ...        import jni
from ...jvm.jframe  import JFrame
from ...jvm.jstring import JString

from ._jvm    import JVM
from ._jclass import JavaClass
from .        import types as jtypes


@public
class JavaProxy(object):

    def __init__(self):

        # Create a Java-side proxy for this Python-side object

        jclass = JVM.jvm.JClass(None, self.__class__.__javaclass__, borrowed=True)

        with JVM.jvm as (jvm, jenv), JFrame(jenv, 4): # cloader, interfaces, ihandler, jproxy
            try:
                cloader  = jenv.CallObjectMethod(jclass.handle, jvm.Class.getClassLoader)
                interfaces = jenv.NewObjectArray(1, jvm.Class.Class)
                jenv.SetObjectArrayElement(interfaces, 0, jclass.handle)
                jargs = jni.new_array(jni.jvalue, 1)
                jargs[0].j = id(self)
                ihandler = jenv.NewObject(jvm.jt_reflect_ProxyHandler.Class,
                                          jvm.jt_reflect_ProxyHandler.Constructor, jargs)
                jargs = jni.new_array(jni.jvalue, 3)
                jargs[0].l = cloader
                jargs[1].l = interfaces
                jargs[2].l = ihandler
                jproxy = jenv.CallStaticObjectMethod(jvm.Proxy.Class,
                                                     jvm.Proxy.newProxyInstance, jargs)
            except:
                raise RuntimeError("Unable to create proxy instance.")
            if not jproxy: # <AK> was: if jproxy.value is None:
                raise RuntimeError("Unable to create proxy instance.")
            try:
                jproxy = jtypes.cast(jenv.NewGlobalRef(jproxy), jtypes.jclass)
            except: # <AK> was: if jproxy.value is None:
                raise RuntimeError("Unable to create global reference to proxy instance.")
        self.__javaobject__ = jproxy
        self._as_parameter_ = jproxy

        # Register this Python instance with the proxy cache
        # This is a weak reference because _proxy_cache is a registry,
        # not an actual user of proxy objects. If all references to the
        # proxy disappear, the proxy cache should be cleaned to avoid
        # leaking memory on objects that aren't being used.
        _proxy_cache[id(self)] = self

    # def __del__(self):
    #
    #     # If this object is garbage collected, remove it from the proxy cache.
    #     del _proxy_cache[id(self)]

    def __repr__(self):

        return "<{}: {}>".format(self.__class__.__name__, self.__javaobject__.value)


@public
def dispatch(instance, method, args):

    """The mechanism by which Java can invoke methods in Python.

    This method should be invoked with an:
     * an ID for a Python object
     * a string representing a method name, and
     * a (void *) arrary of arguments. The arguments should be memory
       references to JNI objects.

    The ID is used to look up the instance from the cache of proxy instances
    that have been instantiated; Python method lookup is then used to invoke
    the appropriate method, and provide the arguments (after casting to
    valid Python objects).

    This method has no return value, so it can only be used to represent Java
    interface methods with no return value.
    """
    try:
        pyinstance = _proxy_cache[instance]
        signatures = pyinstance._methods.get(method)
        if len(signatures) != 1:
            raise RuntimeError("Can't handle multiple prototypes for same method name (yet!)")
        signature = list(signatures)[0]
        if len(args) != len(signature):
            raise RuntimeError("argc provided for dispatch doesn't match registered method.")
        try:
            pymethod = getattr(pyinstance, method)
            pyargs   = [dispatch_cast(jarg, type_signature)
                        for jarg, type_signature in zip(args, signature)]
            pymethod(*pyargs)
        except Exception:
            traceback.print_exc()
    except KeyError:
        raise RuntimeError("Unknown Python instance {}".format(instance))


@public
def dispatch_cast(raw, type_signature):

    """Convert a raw argument provided via a callback into a Python object matching the provided signature.

    This is used by the callback dispatch mechanism. The values passed back will
    be raw pointers to Java objects (even primitives are passed as pointers).
    They need to be converted into Python objects to be passed to the proxied
    interface implementation.
    """
    type_manager = JVM.jvm.type_manager
    thandler = type_manager.get_handler(type_signature)
    if type_signature in ("Z", "C", "B", "S", "I", "J", "F", "D"):
        jobject = JVM.jvm.JObject(None, raw, borrowed=True)
        return thandler.toPython(jobject)
    elif type_signature == "Ljava/lang/String;":
        return thandler.toPython(raw)
    elif type_signature.startswith("L"):
        if raw:
            java_class = JavaClass(type_signature[1:-1])
            with JVM.jvm as (jvm, jenv):
                return java_class(jni=jtypes.cast(jenv.NewGlobalRef(raw), jtypes.jclass))
        else:
            return None
    else:
        raise ValueError("Don't know how to convert argument with type signature '{}'".format(
                         type_signature))


# A cache of known JavaInterface proxies. This is used by the dispatch
# mechanism to direct callbacks to the right place.
_proxy_cache = {}
