# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from . import types as jtypes
from ._jclass  import JavaClass


def return_cast(raw, return_signature):

    """Convert the return value from a JNI call into a Python value.

    The raw value is the value returned by the JNI call; the value returned
    by this method will be converted to match the provided signature.

    Primitive types are returned in the right format, and are not modified.
    Strings are turned into Python unicode objects.
    Objects are provided as JNI references, which are wrapped into an
    instance of the relevant JavaClass.
    """
    if return_signature in ("V", "Z", "C", "B", "S", "I", "J", "F", "D"):

        return raw

    elif return_signature == "Ljava/lang/String;":

        # Check for NULL return values
        return java.GetStringUTFChars(cast(raw, jtypes.jstring), None).decode("utf-8") if raw.value else None

    elif return_signature.startswith("L"):

        # Check for NULL return values
        if not raw.value:
            return None
        java_class = JavaClass(return_signature[1:-1])
        return java_class(jni=raw)

    else:
        raise ValueError("Don't know how to cast return signature '{}'".format(return_signature))
