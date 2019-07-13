# Copyright (c) 2016-2019, Adam Karpierz
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

public(jobject = jni.jobject)
#class jobject(jni.jobject):
#    pass

public(jclass = jobject)
#class jclass(jobject):
#    pass

public(jthrowable = jobject)
#class jthrowable(jobject):
#    pass

public(jstring = jobject)
#class jstring(jobject):
#    pass

public(jarray = jobject)
#class jarray(jobject):
#    pass

public(jbooleanArray = jarray)
#class jbooleanArray(jarray):
#    pass

public(jcharArray = jarray)
#class jcharArray(jarray):
#    pass

public(jbyteArray = jarray)
#class jbyteArray(jarray):
#    pass

public(jshortArray = jarray)
#class jshortArray(jarray):
#    pass

public(jintArray = jarray)
#class jintArray(jarray):
#    pass

public(jlongArray = jarray)
#class jlongArray(jarray):
#    pass

public(jfloatArray = jarray)
#class jfloatArray(jarray):
#    pass

public(jdoubleArray = jarray)
#class jdoubleArray(jarray):
#    pass

public(jobjectArray = jarray)
#class jobjectArray(jarray):
#    pass

public(jweak = jobject)
#class jweak(jobject):
#    pass

public(jmethodID = jobject)
#class jmethodID(jobject):
#    pass

public(jfieldID = jobject)
#class jfieldID(jobject):
#    pass

public(JNINativeMethod   = jni.JNINativeMethod)
public(JNINativeMethod_p = jni.POINTER(JNINativeMethod))

public(JavaVM   = jni.JavaVM)
public(JavaVM_p = jni.POINTER(JavaVM))

public(JNIEnv = jni.JNIEnv)

del public, jni
