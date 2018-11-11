# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import public
from ...        import jni

cast = jni.cast

public(jboolean = jni.jboolean) # c_bool # ct.c_ubyte
public(jchar    = jni.jchar)
public(jbyte    = jni.jbyte)
public(jshort   = jni.jshort)
public(jint     = jni.jint)
public(jlong    = jni.jlong)
public(jfloat   = jni.jfloat)
public(jdouble  = jni.jdouble)
public(jsize    = jni.jsize)

public(jboolean_p = jni.POINTER(jboolean))
public(jchar_p    = jni.POINTER(jchar))
public(jbyte_p    = jni.POINTER(jbyte))
public(jshort_p   = jni.POINTER(jshort))
public(jint_p     = jni.POINTER(jint))
public(jlong_p    = jni.POINTER(jlong))
public(jfloat_p   = jni.POINTER(jfloat))
public(jdouble_p  = jni.POINTER(jdouble))

@public
class jobject(jni.jobject):
    pass

@public
class jclass(jobject):
    pass

@public
class jthrowable(jobject):
    pass

@public
class jstring(jobject):
    pass

@public
class jarray(jobject):
    pass

@public
class jbooleanArray(jarray):
    pass

@public
class jcharArray(jarray):
    pass

@public
class jbyteArray(jarray):
    pass

@public
class jshortArray(jarray):
    pass

@public
class jintArray(jarray):
    pass

@public
class jlongArray(jarray):
    pass

@public
class jfloatArray(jarray):
    pass

@public
class jdoubleArray(jarray):
    pass

@public
class jobjectArray(jarray):
    pass

@public
class jweak(jobject):
    pass

@public
class jmethodID(jobject):
    pass

@public
class jfieldID(jobject):
    pass

public(JNINativeMethod   = jni.JNINativeMethod)
public(JNINativeMethod_p = jni.POINTER(JNINativeMethod))

public(JavaVM   = jni.JavaVM)
public(JavaVM_p = jni.POINTER(JavaVM))

public(JNIEnv = jni.JNIEnv)

del public, jni
