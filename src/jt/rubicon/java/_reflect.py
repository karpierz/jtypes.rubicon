# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from . import types as jtypes


class _ReflectionAPI(object):

    """A lazy-loading proxy for the key classes and methods in the Java reflection API"""

    def __init__(self):

        self._attrs = {}
        self._descriptors = {

            'Class': ('FindClass', 'java/lang/Class'),
            'Class__getName':         ('GetMethodID', 'Class', 'getName',         '()Ljava/lang/String;'),
            'Class__getConstructors': ('GetMethodID', 'Class', 'getConstructors', '()[Ljava/lang/reflect/Constructor;'),
            'Class__getMethods':      ('GetMethodID', 'Class', 'getMethods',      '()[Ljava/lang/reflect/Method;'),
            'Class__getInterfaces':   ('GetMethodID', 'Class', 'getInterfaces',   '()[Ljava/lang/Class;'),
            'Class__getSuperclass':   ('GetMethodID', 'Class', 'getSuperclass',   '()Ljava/lang/Class;'),

            'Constructor': ('FindClass', 'java/lang/reflect/Constructor'),
            'Constructor__getParameterTypes': ('GetMethodID', 'Constructor', 'getParameterTypes', '()[Ljava/lang/Class;'),
            'Constructor__getModifiers':      ('GetMethodID', 'Constructor', 'getModifiers',      '()I'),

            'Method': ('FindClass', 'java/lang/reflect/Method'),
            'Method__getName':           ('GetMethodID', 'Method', 'getName',           '()Ljava/lang/String;'),
            'Method__getReturnType':     ('GetMethodID', 'Method', 'getReturnType',     '()Ljava/lang/Class;'),
            'Method__getParameterTypes': ('GetMethodID', 'Method', 'getParameterTypes', '()[Ljava/lang/Class;'),
            'Method__getModifiers':      ('GetMethodID', 'Method', 'getModifiers',      '()I'),

            'Field': ('FindClass', 'java/lang/reflect/Field'),
            'Field__getType': ('GetMethodID', 'Field', 'getType', '()Ljava/lang/Class;'),

            'Modifier': ('FindClass', 'java/lang/reflect/Modifier'),
            'Modifier__isStatic': ('GetStaticMethodID', 'Modifier', 'isStatic', '(I)Z'),
            'Modifier__isPublic': ('GetStaticMethodID', 'Modifier', 'isPublic', '(I)Z'),

            'Python': ('FindClass', 'org/pybee/rubicon/Python'),
            'Python__proxy':      ('GetStaticMethodID', 'Python', 'proxy',      '(Ljava/lang/Class;J)Ljava/lang/Object;'),
            'Python__getField':   ('GetStaticMethodID', 'Python', 'getField',   '(Ljava/lang/Class;Ljava/lang/String;Z)Ljava/lang/reflect/Field;'),
            'Python__getMethods': ('GetStaticMethodID', 'Python', 'getMethods', '(Ljava/lang/Class;Ljava/lang/String;Z)[Ljava/lang/reflect/Method;'),

            'Boolean': ('FindClass', 'java/lang/Boolean'),
            'Boolean__booleanValue': ('GetMethodID', 'Boolean', 'booleanValue', '()Z'),

            'Byte': ('FindClass', 'java/lang/Byte'),
            'Byte__byteValue': ('GetMethodID', 'Byte', 'byteValue', '()B'),

            'Char': ('FindClass', 'java/lang/Char'),
            'Char__charValue': ('GetMethodID', 'Char', 'charValue', '()C'),

            'Short': ('FindClass', 'java/lang/Short'),
            'Short__shortValue': ('GetMethodID', 'Short', 'shortValue', '()S'),

            'Integer': ('FindClass', 'java/lang/Integer'),
            'Integer__intValue': ('GetMethodID', 'Integer', 'intValue', '()I'),

            'Long': ('FindClass', 'java/lang/Long'),
            'Long__longValue': ('GetMethodID', 'Long', 'longValue', '()J'),

            'Float': ('FindClass', 'java/lang/Float'),
            'Float__floatValue': ('GetMethodID', 'Float', 'floatValue', '()F'),

            'Double': ('FindClass', 'java/lang/Double'),
            'Double__doubleValue': ('GetMethodID', 'Double', 'doubleValue', '()D'),
        }

    def __getattr__(self, name):

        try:
            return self._attrs[name]
        except KeyError:
            try:
                args = self._descriptors[name]

                if args[0] == "FindClass":

                    result = java.FindClass(*args[1:])
                    if result.value is None:
                        raise RuntimeError("Couldn't find Java class '{}'".format(args[1]))
                    result = cast(java.NewGlobalRef(result), jtypes.jclass)

                elif args[0] == "GetMethodID":

                    klass = getattr(self, args[1])
                    result = java.GetMethodID(klass, *args[2:])
                    if result.value is None:
                        raise RuntimeError("Couldn't find Java method '{}.{}'".format(args[1], args[2]))

                elif args[0] == "GetStaticMethodID":

                    klass = getattr(self, args[1])
                    result = java.GetStaticMethodID(klass, *args[2:])
                    if result.value is None:
                        raise RuntimeError("Couldn't find Java static method '{}.{}'".format(args[1], args[2]))

                self._attrs[name] = result
                return result
            except KeyError:
                raise RuntimeError("Unexpected reflection API request '{}'".format(name))
