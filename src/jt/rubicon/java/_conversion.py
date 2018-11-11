# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import

import itertools

from ...jvm.lib import annotate, Optional
from ...jvm.lib import public
from ...jvm.jframe  import JFrame
from ...jvm.jstring import JString

from ._constants import EJavaType
from ._jvm       import JVM
from .           import types as jtypes


###########################################################################
# Signature handling
#
# Methods to convert argument lists into a signature, and vice versa
###########################################################################

@public
def convert_args(args, type_names):

    """Convert a list of arguments to be in a format compliant with the JNI signature.

    This means:
     * casting primitives into the apprpriate jXXX ctypes objects,
     * Strings into Java string objects, and
     * JavaInstance/JavaProxy objects into their JNI references.
    """
    from ._jobject import JavaInstance
    from ._jproxy  import JavaProxy

    converted = []
    for type_name, arg in zip(type_names, args):
        if isinstance(arg, jtypes.jboolean):
            converted.append(arg)
        elif isinstance(arg, bool):
            converted.append(jtypes.jboolean(arg))
        elif isinstance(arg, jtypes.jchar):
            converted.append(arg)
        elif isinstance(arg, jtypes.jbyte):
            converted.append(arg)
        elif isinstance(arg, jtypes.jshort):
            converted.append(arg)
        elif isinstance(arg, jtypes.jint):
            converted.append(arg)
        elif isinstance(arg, int):
            if type_name == "I":
                converted.append(jtypes.jint(arg))
            elif type_name == "J":
                converted.append(jtypes.jlong(arg))
            elif type_name == "S":
                converted.append(jtypes.jshort(arg))
            else:
                raise ValueError("Unexpected type name for int argument.")
        elif isinstance(arg, jtypes.jlong):
            converted.append(arg)
        elif isinstance(arg, jtypes.jfloat):
            converted.append(arg)
        elif isinstance(arg, float):
            if type_name == "F":
                converted.append(jtypes.jfloat(arg))
            elif type_name == "D":
                converted.append(jtypes.jdouble(arg))
            else:
                raise ValueError("Unexpected type name for float argument.")
        elif isinstance(arg, jtypes.jdouble):
            converted.append(arg)
        elif isinstance(arg, (str, type(u""))):
            with JVM.jvm as (_, jenv):
                jstr = jenv.NewStringUTF(arg.encode("utf-8"))
                converted.append(jtypes.jstring(jstr))
        elif isinstance(arg, JavaInstance):
            converted.append(arg.__javaobject__)
        elif isinstance(arg, JavaProxy):
            converted.append(arg.__javaobject__)
        else:
            raise ValueError("Unknown argument type", arg, type(arg))

    return converted


def _convert_args_to_jargs(args, type_names):

    largs = convert_args(args, type_names)
    jargs = JVM.jvm.JArguments(len(largs))
    for pos, jarg in enumerate(largs):
        if isinstance(jarg, jtypes.jboolean):
            jargs.setBoolean(pos, jarg)
        elif isinstance(jarg, jtypes.jchar):
            jargs.setChar(pos, jarg)
        elif isinstance(jarg, jtypes.jbyte):
            jargs.setByte(pos, jarg)
        elif isinstance(jarg, jtypes.jshort):
            jargs.setShort(pos, jarg)
        elif isinstance(jarg, jtypes.jint):
            jargs.setInt(pos, jarg)
        elif isinstance(jarg, jtypes.jlong):
            jargs.setLong(pos, jarg)
        elif isinstance(jarg, jtypes.jfloat):
            jargs.setFloat(pos, jarg)
        elif isinstance(jarg, jtypes.jdouble):
            jargs.setDouble(pos, jarg)
        elif isinstance(jarg, jtypes.jstring):
            jobject = JVM.jvm.JObject(None, jarg, borrowed=True)
            jargs.setObject(pos, jobject)
            jargs.argtypes[pos] = EJavaType.STRING
        else:
            jobject = JVM.jvm.JObject(None, jarg, borrowed=True)
            jargs.setObject(pos, jobject)

    return jargs


@public
def select_polymorph(polymorphs, args):

    """Determine the polymorphic signature that will match a given argument list.

    This is the mechanism used to reconcile Java's strict-typing polymorphism with
    Python's unique-name, weak typing polymorphism. When invoking a method on the
    Python side, the number and types of the arguments provided are used to determine
    which Java method will be invoked.

    polymorphs should be a dictionary, keyed by the JNI signature of the arguments
    expected by the method. The values in the dictionary are not used; this method
    is only used to determine, which key should be used.

    args is a list of arguments that have been passed to invoke the method.

    Returns a 3-tuple:
     * arg_sig - the actual signature of the provided arguments
     * match_types - the type list that was matched. This is a list of individual
       type signatures; not in string form like arg_sig, but as a list where each
       element is the type for a particular argument. (i.e.,
        ['I', 'Ljava/lang/String;', 'Z'], not 'ILjava/langString;Z').

       The contents of match_types will be the same as arg_sig if there is a
       direct match in polymorphs; if there isn't, the signature of the matching
       polymorph will be returned.
     * polymorph - the value from the input polymorphs that matched. Equivalent
       to polymorphs[match_types]
    """
    from ._jobject import JavaInstance
    from ._jproxy  import JavaProxy

    arg_types = []
    if len(args) == 0:
        arg_sig = ""
        options = [[]]
    else:
        for arg in args:
            if isinstance(arg, (bool, jtypes.jboolean)):
                arg_types.append(["Z"])
            elif isinstance(arg, jtypes.jchar):
                arg_types.append(["C"])
            elif isinstance(arg, jtypes.jbyte):
                arg_types.append(["B"])
            elif isinstance(arg, jtypes.jshort):
                arg_types.append(["S"])
            elif isinstance(arg, jtypes.jint):
                arg_types.append(["I"])
            elif isinstance(arg, int):
                arg_types.append(["I", "J", "S"])
            elif isinstance(arg, jtypes.jlong):
                arg_types.append(["J"])
            elif isinstance(arg, jtypes.jfloat):
                arg_types.append(["F"])
            elif isinstance(arg, jtypes.jdouble):
                arg_types.append(["D"])
            elif isinstance(arg, float):
                arg_types.append(["D", "F"])
            elif isinstance(arg, (str, type(u""))):
                arg_types.append([
                    "Ljava/lang/String;",
                    "Ljava/io/Serializable;",
                    "Ljava/lang/Comparable;",
                    "Ljava/lang/CharSequence;",
                    "Ljava/lang/Object;",
                ])
            elif isinstance(arg, (JavaInstance, JavaProxy)):
                arg_types.append(arg.__class__.__dict__["_alternates"])
            else:
                raise ValueError("Unknown argument type", arg, type(arg))

        arg_sig = "".join(t[0] for t in arg_types)

        options = list(itertools.product(*arg_types))

    for option in options:
        try:
            return arg_sig, option, polymorphs["".join(option)]
        except KeyError:
            pass

    raise KeyError(arg_sig)


@public
def signature_for_type_name(type_name):

    """Determine the JNI signature for a given single data type.

    This means a one character representation for primitives, and an
    L<class name>; representation for classes (including String).

    """
    if type_name == "void":
        return "V"
    elif type_name == "boolean":
        return "Z"
    elif type_name == "char":
        return "C"
    elif type_name == "byte":
        return "B"
    elif type_name == "short":
        return "S"
    elif type_name == "int":
        return "I"
    elif type_name == "long":
        return "J"
    elif type_name == "float":
        return "F"
    elif type_name == "double":
        return "D"
    elif type_name.startswith("["):
        return type_name.replace('.', '/')
    else:
        return "L{};".format(type_name.replace('.', '/'))


def _signature_for_type(jclass):

    try:
        type_name = str(jclass.getName())
    except: # <AK> added
        raise RuntimeError("Unable to get name of type.")
    if not type_name: # <AK> was: if type_name.value is None:
        raise RuntimeError("Unable to get name of type.")

    return signature_for_type_name(type_name)


@public
def signature_for_params(params):

    """Determine the JNI-style signature string for an array of Java parameters.

    This is used to convert a Method declaration into a string signature
    that can be used for later lookup.
    """
    return "".join(type_names_for_params(params))


def _signature_for_params(params):

    return "".join(_type_names_for_params(params))


@public
def type_names_for_params(params):

    """Return the Java type descriptors list matching an array of Java parameters.

    This is used when registering interfaces. The params list is converted into a
    tuple, where each element is the JNI type of the parameter.
    """
    signatures = []

    with JVM.jvm as (_, jenv):
        for idx in range(jenv.GetArrayLength(params)):
            with JFrame(jenv, 1): # java_type
                try:
                    java_type = jenv.GetObjectArrayElement(params, idx)
                except:
                    raise RuntimeError("Unable to retrieve parameter type from array.")
                if not java_type: # <AK> was: if java_type.value is None:
                    raise RuntimeError("Unable to retrieve parameter type from array.")
                jclass = JVM.jvm.JClass(None, java_type, borrowed=True)

            try:
                type_name = str(jclass.getName())
            except:
                raise RuntimeError("Unable to get name of type for parameter.")
            if not type_name: # <AK> was: if type_name.value is None:
                raise RuntimeError("Unable to get name of type for parameter.")

            signatures.append(signature_for_type_name(type_name))

    return tuple(signatures)


def _type_names_for_params(params):

    signatures = []

    for jclass in params:
        try:
            type_name = str(jclass.getName())
        except:
            raise RuntimeError("Unable to get name of type for parameter.")
        if not type_name: # <AK> was: if type_name.value is None:
            raise RuntimeError("Unable to get name of type for parameter.")

        signatures.append(signature_for_type_name(type_name))

    return tuple(signatures)


@public
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

        with JVM.jvm as (_, jenv):
            return JString(jenv, raw, borrowed=True).str if raw else None

    elif return_signature.startswith("L"):

        from ._jclass import JavaClass

        if raw:
            java_class = JavaClass(return_signature[1:-1])
            return java_class(jni=jtypes.cast(raw, jtypes.jclass))
        else:
            return None

    else:
        raise ValueError("Don't know how to cast return signature '{}'".format(
                         return_signature))
