# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ._jvm import JVM
from .     import types as jtypes


class _ReflectionAPI(object):

    """A lazy-loading proxy for the key classes and methods in the Java reflection API"""

    def __init__(self):

        self._descriptors = {

            'Class':                          ('FindClass',   'java/lang/Class'),
            'Class__getName':                 ('GetMethodID', 'Class', 'getName',         '()Ljava/lang/String;'),
            'Class__getConstructors':         ('GetMethodID', 'Class', 'getConstructors', '()[Ljava/lang/reflect/Constructor;'),
            'Class__getMethods':              ('GetMethodID', 'Class', 'getMethods',      '()[Ljava/lang/reflect/Method;'),
            'Class__getField':                ('GetMethodID', 'Class', 'getField',        '(Ljava/lang/String;)Ljava/lang/reflect/Field;'), # <AK> added
            'Class__getInterfaces':           ('GetMethodID', 'Class', 'getInterfaces',   '()[Ljava/lang/Class;'),
            'Class__getSuperclass':           ('GetMethodID', 'Class', 'getSuperclass',   '()Ljava/lang/Class;'),

            'Constructor':                    ('FindClass',   'java/lang/reflect/Constructor'),
            'Constructor__getParameterTypes': ('GetMethodID', 'Constructor', 'getParameterTypes', '()[Ljava/lang/Class;'),
            'Constructor__getModifiers':      ('GetMethodID', 'Constructor', 'getModifiers',      '()I'),

            'Method':                         ('FindClass',   'java/lang/reflect/Method'),
            'Method__getName':                ('GetMethodID', 'Method', 'getName',           '()Ljava/lang/String;'),
            'Method__getReturnType':          ('GetMethodID', 'Method', 'getReturnType',     '()Ljava/lang/Class;'),
            'Method__getParameterTypes':      ('GetMethodID', 'Method', 'getParameterTypes', '()[Ljava/lang/Class;'),
            'Method__getModifiers':           ('GetMethodID', 'Method', 'getModifiers',      '()I'),

            'Field':                          ('FindClass',   'java/lang/reflect/Field'),
            'Field__getType':                 ('GetMethodID', 'Field', 'getType',      '()Ljava/lang/Class;'),
            'Field__getModifiers':            ('GetMethodID', 'Field', 'getModifiers', '()I'), # <AK> added

            'Modifier':                       ('FindClass',         'java/lang/reflect/Modifier'),
            'Modifier__isStatic':             ('GetStaticMethodID', 'Modifier', 'isStatic', '(I)Z'),
            'Modifier__isPublic':             ('GetStaticMethodID', 'Modifier', 'isPublic', '(I)Z'),

            'Python':                         ('FindClass',         'org/pybee/rubicon/Python'),

            'Boolean':                        ('FindClass',   'java/lang/Boolean'),
            'Boolean__booleanValue':          ('GetMethodID', 'Boolean', 'booleanValue', '()Z'),

            'Char':                           ('FindClass',   'java/lang/Character'),
            'Char__charValue':                ('GetMethodID', 'Char', 'charValue', '()C'),

            'Byte':                           ('FindClass',   'java/lang/Byte'),
            'Byte__byteValue':                ('GetMethodID', 'Byte', 'byteValue', '()B'),

            'Short':                          ('FindClass',   'java/lang/Short'),
            'Short__shortValue':              ('GetMethodID', 'Short', 'shortValue', '()S'),

            'Integer':                        ('FindClass',   'java/lang/Integer'),
            'Integer__intValue':              ('GetMethodID', 'Integer', 'intValue', '()I'),

            'Long':                           ('FindClass',   'java/lang/Long'),
            'Long__longValue':                ('GetMethodID', 'Long', 'longValue', '()J'),

            'Float':                          ('FindClass',   'java/lang/Float'),
            'Float__floatValue':              ('GetMethodID', 'Float', 'floatValue', '()F'),

            'Double':                         ('FindClass',   'java/lang/Double'),
            'Double__doubleValue':            ('GetMethodID', 'Double', 'doubleValue', '()D'),
        }

    def __getattr__(self, name):

        try:
            return self._attrs[name]
        except KeyError:
            try:
                descriptor = self._descriptors[name]
                descr_type = descriptor[0]
                arguments  = descriptor[1:]

                if descr_type == "FindClass":

                    class_name, = arguments
                    name_trans = JVM.jvm.JClass.name_trans
                    class_name = class_name.encode("utf-8").translate(name_trans).decode("utf-8")
                    try:
                        jclass = JVM.jvm.JClass.forName(class_name)
                    except:
                        raise RuntimeError("Couldn't find Java class '{}'".format(class_name))
                    with JVM.jvm as (_, jenv):
                        result = jtypes.cast(jenv.NewGlobalRef(jclass.handle), jtypes.jclass)

                elif descr_type == "GetMethodID":

                    class_name, method_name, method_signature = arguments
                    jclass = getattr(self, class_name)
                    with JVM.jvm as (_, jenv):
                        try:
                            result = jenv.GetMethodID(jclass, method_name.encode("utf-8"), method_signature.encode("utf-8"))
                        except: # <AK> was: if result.value is None:
                            raise RuntimeError("Couldn't find Java method '{}.{}'".format(class_name, method_name))

                elif descr_type == "GetStaticMethodID":

                    class_name, method_name, method_signature = arguments
                    jclass = getattr(self, class_name)
                    with JVM.jvm as (_, jenv):
                        try:
                            result = jenv.GetStaticMethodID(jclass, method_name.encode("utf-8"), method_signature.encode("utf-8"))
                        except: # <AK> was: if result.value is None:
                            raise RuntimeError("Couldn't find Java static method '{}.{}'".format(class_name, method_name))

                self._attrs[name] = result
                return result
            except KeyError:
                raise RuntimeError("Unexpected reflection API request '{}'".format(name))


reflect = _ReflectionAPI()
