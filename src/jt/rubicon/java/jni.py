from __future__ import absolute_import

from ctypes    import *
from ctypes    import util
from functools import partial

from ... import jni

from .types    import *
from ._reflect import reflect
from ._jvm     import JVM

JNI_VERSION_1_1 = jni.JNI_VERSION_1_1
JNI_VERSION_1_2 = jni.JNI_VERSION_1_2
JNI_VERSION_1_4 = jni.JNI_VERSION_1_4
JNI_VERSION_1_6 = jni.JNI_VERSION_1_6
JNI_VERSION_1_8 = jni.JNI_VERSION_1_8  # <AK> added
JNI_VERSION_9   = jni.JNI_VERSION_9    # <AK> added
JNI_VERSION_10  = jni.JNI_VERSION_10   # <AK> added

# Standard JNI API

class jaga:
    pass

#java.GetVersion.restype  = jint
#java.GetVersion.argtypes = []
jaga.GetVersion = lambda *args: jni.jint(JVM.jenv.functions[0].GetVersion(JVM.jenv, *args))

#java.DefineClass.restype  = jclass
#java.DefineClass.argtypes = [c_char_p, jobject, jbyte_p, jsize]
jaga.DefineClass = lambda *args: JVM.jenv.functions[0].DefineClass(JVM.jenv, *args)
#java.FindClass.restype  = jclass
#java.FindClass.argtypes = [c_char_p]
jaga.FindClass = lambda *args: JVM.jenv.functions[0].FindClass(JVM.jenv, *args)

#java.FromReflectedMethod.restype  = jmethodID
#java.FromReflectedMethod.argtypes = [jobject]
#java.FromReflectedField.restype  = jfieldID
#java.FromReflectedField.argtypes = [jobject]
#java.ToReflectedMethod.restype  = jobject
#java.ToReflectedMethod.argtypes = [jclass, jmethodID, jboolean]

#java.GetSuperclass.restype  = jclass
#java.GetSuperclass.argtypes = [jclass]
#java.IsAssignableFrom.restype  = jboolean
#java.IsAssignableFrom.argtypes = [jclass, jclass]

#java.ToReflectedField.restype  = jobject
#java.ToReflectedField.argtypes = [jclass, jfieldID, jboolean]

#java.Throw.restype  = jint
#java.Throw.argtypes = [jthrowable]
#java.ThrowNew.restype  = jint
#java.ThrowNew.argtypes = [jclass, c_char_p]
#java.ExceptionOccurred.restype  = jthrowable
#java.ExceptionOccurred.argtypes = []
#java.ExceptionDescribe.restype  = None
#java.ExceptionDescribe.argtypes = []
#java.ExceptionClear.restype  = None
#java.ExceptionClear.argtypes = []
#java.FatalError.restype  = None
#java.FatalError.argtypes = [c_char_p]

#java.PushLocalFrame.restype  = jint
#java.PushLocalFrame.argtypes = [jint]
#java.PopLocalFrame.restype  = jobject
#java.PopLocalFrame.argtypes = [jobject]

#java.NewGlobalRef.restype  = jobject
#java.NewGlobalRef.argtypes = [jobject]
jaga.NewGlobalRef = lambda *args: JVM.jenv.functions[0].NewGlobalRef(JVM.jenv, *args)
#java.DeleteGlobalRef.restype  = None
#java.DeleteGlobalRef.argtypes = [jobject]
jaga.DeleteGlobalRef = lambda *args: JVM.jenv.functions[0].DeleteGlobalRef(JVM.jenv, *args)
#java.DeleteLocalRef.restype  = None
#java.DeleteLocalRef.argtypes = [jobject]
jaga.DeleteLocalRef = lambda *args: JVM.jenv.functions[0].DeleteLocalRef(JVM.jenv, *args)

#java.IsSameObject.restype  = jboolean
#java.IsSameObject.argtypes = [jobject, jobject]

#java.NewLocalRef.restype  = jobject
#java.NewLocalRef.argtypes = [jobject]
#java.EnsureLocalCapacity.restype  = jint
#java.EnsureLocalCapacity.argtypes = [jint]

#java.AllocObject.restype  = jobject
#java.AllocObject.argtypes = [jclass]
#java.NewObject.restype  = jobject
#java.NewObject.argtypes = [jclass, jmethodID]
jaga.NewObject = lambda *args: JVM.jenv.functions[0].NewObject(JVM.jenv, *args)

#java.GetObjectClass.restype  = jclass
#java.GetObjectClass.argtypes = [jobject]
#java.IsInstanceOf.restype  = jboolean
#java.IsInstanceOf.argtypes = [jobject, jclass]

#java.GetMethodID.restype  = jmethodID
#java.GetMethodID.argtypes = [jclass, c_char_p, c_char_p]
jaga.GetMethodID = lambda *args: JVM.jenv.functions[0].GetMethodID(JVM.jenv, *args)

#java.CallObjectMethod.restype  = jobject
#java.CallObjectMethod.argtypes = [jobject, jmethodID]
jaga.CallObjectMethod = lambda *args: JVM.jenv.functions[0].CallObjectMethod(JVM.jenv, *args)
#java.CallBooleanMethod.restype  = jboolean
#java.CallBooleanMethod.argtypes = [jobject, jmethodID]
jaga.CallBooleanMethod = lambda *args: JVM.jenv.functions[0].CallBooleanMethod(JVM.jenv, *args)
#java.CallByteMethod.restype  = jbyte
#java.CallByteMethod.argtypes = [jobject, jmethodID]
jaga.CallByteMethod = lambda *args: JVM.jenv.functions[0].CallByteMethod(JVM.jenv, *args)
#java.CallCharMethod.restype  = jchar
#java.CallCharMethod.argtypes = [jobject, jmethodID]
jaga.CallCharMethod = lambda *args: JVM.jenv.functions[0].CallCharMethod(JVM.jenv, *args)
#java.CallShortMethod.restype  = jshort
#java.CallShortMethod.argtypes = [jobject, jmethodID]
jaga.CallShortMethod = lambda *args: JVM.jenv.functions[0].CallShortMethod(JVM.jenv, *args)
#java.CallIntMethod.restype  = jint
#java.CallIntMethod.argtypes = [jobject, jmethodID]
jaga.CallIntMethod = lambda *args: JVM.jenv.functions[0].CallIntMethod(JVM.jenv, *args)
#java.CallLongMethod.restype  = jlong
#java.CallLongMethod.argtypes = [jobject, jmethodID]
jaga.CallLongMethod = lambda *args: JVM.jenv.functions[0].CallLongMethod(JVM.jenv, *args)
#java.CallFloatMethod.restype  = jfloat
#java.CallFloatMethod.argtypes = [jobject, jmethodID]
jaga.CallFloatMethod = lambda *args: JVM.jenv.functions[0].CallFloatMethod(JVM.jenv, *args)
#java.CallDoubleMethod.restype  = jdouble
#java.CallDoubleMethod.argtypes = [jobject, jmethodID]
jaga.CallDoubleMethod = lambda *args: JVM.jenv.functions[0].CallDoubleMethod(JVM.jenv, *args)
#java.CallVoidMethod.restype  = None
#java.CallVoidMethod.argtypes = [jobject, jmethodID]
jaga.CallVoidMethod = lambda *args: JVM.jenv.functions[0].CallVoidMethod(JVM.jenv, *args)

#java.CallNonvirtualObjectMethod.restype  = jobject
#java.CallNonvirtualObjectMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualBooleanMethod.restype  = jboolean
#java.CallNonvirtualBooleanMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualByteMethod.restype  = jbyte
#java.CallNonvirtualByteMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualCharMethod.restype  = jchar
#java.CallNonvirtualCharMethod.argtypes = [jobject, jclass,jmethodID]
#java.CallNonvirtualShortMethod.restype  = jshort
#java.CallNonvirtualShortMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualIntMethod.restype  = jint
#java.CallNonvirtualIntMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualLongMethod.restype  = jlong
#java.CallNonvirtualLongMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualFloatMethod.restype  = jfloat
#java.CallNonvirtualFloatMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualDoubleMethod.restype  = jdouble
#java.CallNonvirtualDoubleMethod.argtypes = [jobject, jclass, jmethodID]
#java.CallNonvirtualVoidMethod.restype  = None
#java.CallNonvirtualVoidMethod.argtypes = [jobject, jclass, jmethodID]

#java.GetFieldID.restype  = jfieldID
#java.GetFieldID.argtypes = [jclass, c_char_p, c_char_p]
jaga.GetFieldID = lambda *args: JVM.jenv.functions[0].GetFieldID(JVM.jenv, *args)

#java.GetObjectField.restype  = jobject
#java.GetObjectField.argtypes = [jobject, jfieldID]
#java.GetBooleanField.restype  = jboolean
#java.GetBooleanField.argtypes = [jobject, jfieldID]
#java.GetByteField.restype  = jbyte
#java.GetByteField.argtypes = [jobject, jfieldID]
#java.GetCharField.restype  = jchar
#java.GetCharField.argtypes = [jobject, jfieldID]
#java.GetShortField.restype  = jshort
#java.GetShortField.argtypes = [jobject, jfieldID]
#java.GetIntField.restype  = jint
#java.GetIntField.argtypes = [jobject, jfieldID]
jaga.GetIntField = lambda *args: JVM.jenv.functions[0].GetIntField(JVM.jenv, *args)
#java.GetLongField.restype  = jlong
#java.GetLongField.argtypes = [jobject, jfieldID]
#java.GetFloatField.restype  = jfloat
#java.GetFloatField.argtypes = [jobject, jfieldID]
#java.GetDoubleField.restype  = jdouble
#java.GetDoubleField.argtypes = [jobject, jfieldID]

#java.SetObjectField.restype  = None
#java.SetObjectField.argtypes = [jobject, jfieldID, jobject]
#java.SetBooleanField.restype  = None
#java.SetBooleanField.argtypes = [jobject, jfieldID, jboolean]
#java.SetByteField.restype  = None
#java.SetByteField.argtypes = [jobject, jfieldID, jbyte]
#java.SetCharField.restype  = None
#java.SetCharField.argtypes = [jobject, jfieldID, jchar]
#java.SetShortField.restype  = None
#java.SetShortField.argtypes = [jobject, jfieldID, jshort]
#java.SetIntField.restype  = None
#java.SetIntField.argtypes = [jobject, jfieldID, jint]
#java.SetLongField.restype  = None
#java.SetLongField.argtypes = [jobject, jfieldID, jlong]
#java.SetFloatField.restype  = None
#java.SetFloatField.argtypes = [jobject, jfieldID, jfloat]
#java.SetDoubleField.restype  = None
#java.SetDoubleField.argtypes = [jobject, jfieldID, jdouble]

#java.GetStaticMethodID.restype  = jmethodID
#java.GetStaticMethodID.argtypes = [jclass, c_char_p, c_char_p]
jaga.GetStaticMethodID = lambda *args: JVM.jenv.functions[0].GetStaticMethodID(JVM.jenv, *args)

#java.CallStaticObjectMethod.restype  = jobject
#java.CallStaticObjectMethod.argtypes = [jclass, jmethodID]
jaga.CallStaticObjectMethod = lambda *args: JVM.jenv.functions[0].CallStaticObjectMethod(JVM.jenv, *args)
#java.CallStaticBooleanMethod.restype  = jboolean
#java.CallStaticBooleanMethod.argtypes = [jclass, jmethodID]
jaga.CallStaticBooleanMethod = lambda *args: JVM.jenv.functions[0].CallStaticBooleanMethod(JVM.jenv, *args)
#java.CallStaticByteMethod.restype  = jbyte
#java.CallStaticByteMethod.argtypes = [jclass, jmethodID]
#java.CallStaticCharMethod.restype  = jchar
#java.CallStaticCharMethod.argtypes = [jclass, jmethodID]
#java.CallStaticShortMethod.restype  = jshort
#java.CallStaticShortMethod.argtypes = [jclass, jmethodID]
#java.CallStaticIntMethod.restype  = jint
#java.CallStaticIntMethod.argtypes = [jclass, jmethodID]
jaga.CallStaticIntMethod = lambda *args: JVM.jenv.functions[0].CallStaticIntMethod(JVM.jenv, *args)
#java.CallStaticLongMethod.restype  = jlong
#java.CallStaticLongMethod.argtypes = [jclass, jmethodID]
#java.CallStaticFloatMethod.restype  = jfloat
#java.CallStaticFloatMethod.argtypes = [jclass, jmethodID]
#java.CallStaticDoubleMethod.restype  = jdouble
#java.CallStaticDoubleMethod.argtypes = [jclass, jmethodID]
#java.CallStaticVoidMethod.restype  = None
#java.CallStaticVoidMethod.argtypes = [jclass, jmethodID]

#java.GetStaticFieldID.restype  = jfieldID
#java.GetStaticFieldID.argtypes = [jclass, c_char_p, c_char_p]
jaga.GetStaticFieldID = lambda *args: JVM.jenv.functions[0].GetStaticFieldID(JVM.jenv, *args)

#java.GetStaticObjectField.restype  = jobject
#java.GetStaticObjectField.argtypes = [jclass, jfieldID]
#java.GetStaticBooleanField.restype  = jboolean
#java.GetStaticBooleanField.argtypes = [jclass, jfieldID]
#java.GetStaticByteField.restype  = jbyte
#java.GetStaticByteField.argtypes = [jclass, jfieldID]
#java.GetStaticCharField.restype  = jchar
#java.GetStaticCharField.argtypes = [jclass, jfieldID]
#java.GetStaticShortField.restype  = jshort
#java.GetStaticShortField.argtypes = [jclass, jfieldID]
#java.GetStaticIntField.restype  = jint
#java.GetStaticIntField.argtypes = [jclass, jfieldID]
jaga.GetStaticIntField = lambda *args: JVM.jenv.functions[0].GetStaticIntField(JVM.jenv, *args)
#java.GetStaticLongField.restype  = jlong
#java.GetStaticLongField.argtypes = [jclass, jfieldID]
#java.GetStaticFloatField.restype  = jfloat
#java.GetStaticFloatField.argtypes = [jclass, jfieldID]
#java.GetStaticDoubleField.restype  = jdouble
#java.GetStaticDoubleField.argtypes = [jclass, jfieldID]

#java.SetStaticObjectField.restype  = None
#java.SetStaticObjectField.argtypes = [jclass, jfieldID, jobject]
#java.SetStaticBooleanField.restype  = None
#java.SetStaticBooleanField.argtypes = [jclass, jfieldID, jboolean]
#java.SetStaticByteField.restype  = None
#java.SetStaticByteField.argtypes = [jclass, jfieldID, jbyte]
#java.SetStaticCharField.restype  = None
#java.SetStaticCharField.argtypes = [jclass, jfieldID, jchar]
#java.SetStaticShortField.restype  = None
#java.SetStaticShortField.argtypes = [jclass, jfieldID, jshort]
#java.SetStaticIntField.restype  = None
#java.SetStaticIntField.argtypes = [jclass, jfieldID, jint]
#java.SetStaticLongField.restype  = None
#java.SetStaticLongField.argtypes = [jclass, jfieldID, jlong]
#java.SetStaticFloatField.restype  = None
#java.SetStaticFloatField.argtypes = [jclass, jfieldID, jfloat]
#java.SetStaticDoubleField.restype  = None
#java.SetStaticDoubleField.argtypes = [jclass, jfieldID, jdouble]

#java.NewString.restype  = jstring
#java.NewString.argtypes = [jchar_p, jsize]
#java.GetStringLength.restype  = jsize
#java.GetStringLength.argtypes = [jstring]
#java.GetStringChars.restype  = jchar_p
#java.GetStringChars.argtypes = [jstring, jboolean_p]
#java.ReleaseStringChars.restype  = None
#java.ReleaseStringChars.argtypes = [jstring, jchar_p]

#java.NewStringUTF.restype  = jstring
#java.NewStringUTF.argtypes = [c_char_p]
jaga.NewStringUTF = lambda *args: JVM.jenv.functions[0].NewStringUTF(JVM.jenv, *args)
#java.GetStringUTFLength.restype  = jsize
#java.GetStringUTFLength.argtypes = [jstring]
#java.GetStringUTFChars.restype  = c_char_p
#java.GetStringUTFChars.argtypes = [jstring, jboolean_p]
jaga.GetStringUTFChars = lambda *args: JVM.jenv.functions[0].GetStringUTFChars(JVM.jenv, *args)
#java.ReleaseStringUTFChars.restype  = None
#java.ReleaseStringUTFChars.argtypes = [jstring, c_char_p]
jaga.ReleaseStringUTFChars = lambda *args: JVM.jenv.functions[0].ReleaseStringUTFChars(JVM.jenv, *args)

#java.GetArrayLength.restype  = jsize
#java.GetArrayLength.argtypes = [jarray]
jaga.GetArrayLength = lambda *args: JVM.jenv.functions[0].GetArrayLength(JVM.jenv, *args)
#java.NewObjectArray.restype  = jobjectArray
#java.NewObjectArray.argtypes = [jsize, jclass, jobject]
#java.GetObjectArrayElement.restype  = jobject
#java.GetObjectArrayElement.argtypes = [jobjectArray, jsize]
jaga.GetObjectArrayElement = lambda *args: JVM.jenv.functions[0].GetObjectArrayElement(JVM.jenv, *args)
#java.SetObjectArrayElement.restype  = None
#java.SetObjectArrayElement.argtypes = [jobjectArray, jsize, jobject]

#java.NewBooleanArray.restype  = jbooleanArray
#java.NewBooleanArray.argtypes = [jsize]
#java.NewByteArray.restype  = jbyteArray
#java.NewByteArray.argtypes = [jsize]
#java.NewCharArray.restype  = jcharArray
#java.NewCharArray.argtypes = [jsize]
#java.NewShortArray.restype  = jshortArray
#java.NewShortArray.argtypes = [jsize]
#java.NewIntArray.restype  = jintArray
#java.NewIntArray.argtypes = [jsize]
#java.NewLongArray.restype  = jlongArray
#java.NewLongArray.argtypes = [jsize]
#java.NewFloatArray.restype  = jfloatArray
#java.NewFloatArray.argtypes = [jsize]
#java.NewDoubleArray.restype  = jdoubleArray
#java.NewDoubleArray.argtypes = [jsize]

#java.GetBooleanArrayElements.restype  = jboolean_p
#java.GetBooleanArrayElements.argtypes = [jbooleanArray, jboolean_p]
#java.GetByteArrayElements.restype  = jbyte_p
#java.GetByteArrayElements.argtypes = [jbyteArray, jboolean_p]
#java.GetCharArrayElements.restype  = jchar_p
#java.GetCharArrayElements.argtypes = [jcharArray, jboolean_p]
#java.GetShortArrayElements.restype  = jshort_p
#java.GetShortArrayElements.argtypes = [jshortArray, jboolean_p]
#java.GetIntArrayElements.restype  = jint_p
#java.GetIntArrayElements.argtypes = [jintArray, jboolean_p]
#java.GetLongArrayElements.restype  = jlong_p
#java.GetLongArrayElements.argtypes = [jlongArray, jboolean_p]
#java.GetFloatArrayElements.restype  = jfloat_p
#java.GetFloatArrayElements.argtypes = [jfloatArray, jboolean_p]
#java.GetDoubleArrayElements.restype  = jdouble_p
#java.GetDoubleArrayElements.argtypes = [jdoubleArray, jboolean_p]

#java.ReleaseBooleanArrayElements.restype  = None
#java.ReleaseBooleanArrayElements.argtypes = [jbooleanArray, jboolean_p, jint]
#java.ReleaseByteArrayElements.restype  = None
#java.ReleaseByteArrayElements.argtypes = [jbyteArray, jbyte_p, jint]
#java.ReleaseCharArrayElements.restype  = None
#java.ReleaseCharArrayElements.argtypes = [jcharArray, jchar_p, jint]
#java.ReleaseShortArrayElements.restype  = None
#java.ReleaseShortArrayElements.argtypes = [jshortArray, jshort_p, jint]
#java.ReleaseIntArrayElements.restype  = None
#java.ReleaseIntArrayElements.argtypes = [jintArray, jint_p, jint]
#java.ReleaseLongArrayElements.restype  = None
#java.ReleaseLongArrayElements.argtypes = [jlongArray, jlong_p, jint]
#java.ReleaseFloatArrayElements.restype  = None
#java.ReleaseFloatArrayElements.argtypes = [jfloatArray, jfloat_p, jint]
#java.ReleaseDoubleArrayElements.restype  = None
#java.ReleaseDoubleArrayElements.argtypes = [jdoubleArray, jdouble_p, jint]

#java.GetBooleanArrayRegion.restype  = None
#java.GetBooleanArrayRegion.argtypes = [jbooleanArray, jsize, jsize, jboolean_p]
#java.GetByteArrayRegion.restype  = None
#java.GetByteArrayRegion.argtypes = [jbyteArray, jsize, jsize, jbyte_p]
#java.GetCharArrayRegion.restype  = None
#java.GetCharArrayRegion.argtypes = [jcharArray, jsize, jsize, jchar_p]
#java.GetShortArrayRegion.restype  = None
#java.GetShortArrayRegion.argtypes = [jshortArray, jsize, jsize, jshort_p]
#java.GetIntArrayRegion.restype  = None
#java.GetIntArrayRegion.argtypes = [jintArray, jsize, jsize, jint_p]
#java.GetLongArrayRegion.restype  = None
#java.GetLongArrayRegion.argtypes = [jlongArray, jsize, jsize, jlong_p]
#java.GetFloatArrayRegion.restype  = None
#java.GetFloatArrayRegion.argtypes = [jfloatArray, jsize, jsize, jfloat_p]
#java.GetDoubleArrayRegion.restype  = None
#java.GetDoubleArrayRegion.argtypes = [jdoubleArray, jsize, jsize, jdouble_p]

#java.SetBooleanArrayRegion.restype  = None
#java.SetBooleanArrayRegion.argtypes = [jbooleanArray, jsize, jsize, jboolean_p]
#java.SetByteArrayRegion.restype  = None
#java.SetByteArrayRegion.argtypes = [jbyteArray, jsize, jsize, jbyte_p]
#java.SetCharArrayRegion.restype  = None
#java.SetCharArrayRegion.argtypes = [jcharArray, jsize, jsize, jchar_p]
#java.SetShortArrayRegion.restype  = None
#java.SetShortArrayRegion.argtypes = [jshortArray, jsize, jsize, jshort_p]
#java.SetIntArrayRegion.restype  = None
#java.SetIntArrayRegion.argtypes = [jintArray, jsize, jsize, jint_p]
#java.SetLongArrayRegion.restype  = None
#java.SetLongArrayRegion.argtypes = [jlongArray, jsize, jsize, jlong_p]
#java.SetFloatArrayRegion.restype  = None
#java.SetFloatArrayRegion.argtypes = [jfloatArray, jsize, jsize, jfloat_p]
#java.SetDoubleArrayRegion.restype  = None
#java.SetDoubleArrayRegion.argtypes = [jdoubleArray, jsize, jsize, jdouble_p]

#java.RegisterNatives.restype  = jint
#java.RegisterNatives.argtypes = [jclass, JNINativeMethod_p, jint]
#java.UnregisterNatives.restype  = jint
#java.UnregisterNatives.argtypes = [jclass]

#java.MonitorEnter.restype  = jint
#java.MonitorEnter.argtypes = [jobject]
#java.MonitorExit.restype  = jint
#java.MonitorExit.argtypes = [jobject]

#java.GetJavaVM.restype  = jint
#java.GetJavaVM.argtypes = [JavaVM_p]

#java.GetStringRegion.restype  = None
#java.GetStringRegion.argtypes = [jstring, jsize, jsize, jchar_p]
#java.GetStringUTFRegion.restype  = None
#java.GetStringUTFRegion.argtypes = [jstring, jsize, jsize, c_char_p]

#java.GetPrimitiveArrayCritical.restype  = c_void_p
#java.GetPrimitiveArrayCritical.argtypes = [jarray, jboolean_p]
#java.ReleasePrimitiveArrayCritical.restype  = None
#java.ReleasePrimitiveArrayCritical.argtypes = [jarray, c_void_p, jint]

#java.GetStringCritical.restype  = jchar_p
#java.GetStringCritical.argtypes = [jstring, jboolean_p]
#java.ReleaseStringCritical.restype  = None
#java.ReleaseStringCritical.argtypes = [jstring, jchar_p]

#java.NewWeakGlobalRef.restype  = jweak
#java.NewWeakGlobalRef.argtypes = [jobject]
#java.DeleteWeakGlobalRef.restype  = None
#java.DeleteWeakGlobalRef.argtypes = [jweak]

#java.ExceptionCheck.restype  = jboolean
#java.ExceptionCheck.argtypes = []

#java.NewDirectByteBuffer.restype  = jobject
#java.NewDirectByteBuffer.argtypes = [c_void_p, jlong]
#java.GetDirectBufferAddress.restype  = c_void_p
#java.GetDirectBufferAddress.argtypes = [jobject]
#java.GetDirectBufferCapacity.restype  = jlong
#java.GetDirectBufferCapacity.argtypes = [jobject]

#java.GetObjectRefType.restype  = c_int
#java.GetObjectRefType.argtypes = [jobject]

java = jaga
