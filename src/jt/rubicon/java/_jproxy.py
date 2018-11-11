# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import

from ...jvm.lib import annotate
from ...jvm.lib import public

from .         import types as jtypes
from ._jclass  import JavaClass
from ._reflect import reflect


@public
class JavaProxy(object):

    def __init__(self):

        # Create a Java-side proxy for this Python-side object

        jclass = self.__class__.__javaclass__
        jobject = java.CallStaticObjectMethod(reflect.Python, reflect.Python__proxy,
                                              jclass, jtypes.jlong(id(self)))
        if jobject.value is None:
            raise RuntimeError("Unable to create proxy instance.")
        jobject = cast(java.NewGlobalRef(jobject), jtypes.jclass)
        if jobject.value is None:
            raise RuntimeError("Unable to create global reference to proxy instance.")
        self.__javaobject__ = jobject
        self._as_parameter_ = jobject

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
        if len(signatures) == 1:
            signature = list(signatures)[0]
            if len(args) != len(signature):
                raise RuntimeError("argc provided for dispatch doesn't match registered method.")
            try:
                pymethod = getattr(pyinstance, method)
                pyargs   = [dispatch_cast(jarg, jtype) for jarg, jtype in zip(args, signature)]
                pymethod(*pyargs)
            except Exception:
                import traceback
                traceback.print_exc()
        else:
            raise RuntimeError("Can't handle multiple prototypes for same method name (yet!)")
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
    if type_signature == "Z":
        return java.CallBooleanMethod(jtypes.jobject(raw), reflect.Boolean__booleanValue)
    elif type_signature == "B":
        return java.CallByteMethod(jtypes.jobject(raw), reflect.Byte__byteValue)
    elif type_signature == "C":
        return java.CallCharMethod(jtypes.jobject(raw), reflect.Char__charValue)
    elif type_signature == "S":
        return java.CallShortMethod(jtypes.jobject(raw), reflect.Short__shortValue)
    elif type_signature == "I":
        return java.CallIntMethod(jtypes.jobject(raw), reflect.Integer__intValue)
    elif type_signature == "J":
        return java.CallLongMethod(jtypes.jobject(raw), reflect.Long__longValue)
    elif type_signature == "F":
        return java.CallFloatMethod(jtypes.jobject(raw), reflect.Float__floatValue)
    elif type_signature == "D":
        return java.CallDoubleMethod(jtypes.jobject(raw), reflect.Double__doubleValue)
    elif type_signature == "Ljava/lang/String;":
        # Check for NULL return values
        return java.GetStringUTFChars(cast(raw, jtypes.jstring), None).decode("utf-8") if c_void_p(raw).value else None
    elif type_signature.startswith("L"):
        # Check for NULL return values
        if not jtypes.jobject(raw).value:
            return None
        gref = java.NewGlobalRef(jtypes.jobject(raw))
        java_class = JavaClass(type_signature[1:-1])
        return java_class(jni=gref)
    else:
        raise ValueError("Don't know how to convert argument with type signature '{}'".format(
                         type_signature))


# A cache of known JavaInterface proxies. This is used by the dispatch
# mechanism to direct callbacks to the right place.
_proxy_cache = {}
