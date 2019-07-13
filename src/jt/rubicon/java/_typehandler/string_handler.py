# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ....jvm.lib.compat import *
from ....jvm.lib import annotate
from ....jvm.lib import public
from ....        import jni
from ....jvm.jstring import JString

from .._constants  import EJavaType
from .._jvm        import JVM

from ._base_handler import _ObjectHandler
from ._base_handler import int_types, str_types


@public
class StringHandler(_ObjectHandler):

    __slots__ = ()

    def __init__(self, state):

        super(StringHandler, self).__init__(state, EJavaType.STRING, "Ljava/lang/String;")

    def match(self, val):

        from .._jclass import JavaClass, JavaObject
        from .._jproxy import PythonJavaClass

        obj_classname = self._jclass[1:-1].replace("/", ".")

        if val is None:
            return EMatchType.PERFECT
        elif obj_classname == "java.lang.String" and isinstance(val, str_types):
            return EMatchType.PERFECT
        elif obj_classname == "java.lang.Object":
            # if it's a generic object, accept python string, or any java class/object
            if isinstance(val, (JavaClass, JavaObject, PythonJavaClass)):
                return EMatchType.PERFECT
            elif isinstance(val, str_types):
                return EMatchType.IMPLICIT
            else:
                return EMatchType.NONE
        elif hasattr(val, "__javaclass__") and obj_classname == "java.lang.Class":
            # accept an autoclass class for java/lang/Class.
            return EMatchType.PERFECT
        else:
            # if we pass a JavaClass, ensure the definition is matching
            # XXX FIXME what if we use a subclass or something ?
            if isinstance(val, JavaClass):
                jc_classname = val.__javaclass__.replace("/", ".")
                if obj_classname == jc_classname:
                    return EMatchType.PERFECT
                else:
                    #from .._conversion import _check_assignable_from
                    #try:
                    #    _check_assignable_from(obj_classname, val)
                    #except:
                    #    return EMatchType.NONE
                    return EMatchType.IMPLICIT
            # always accept unknow object, but can be dangerous too.
            elif isinstance(val, JavaObject):
                return EMatchType.EXPLICIT
            elif isinstance(val, PythonJavaClass):
                return EMatchType.EXPLICIT
            else:
                # native type? not accepted
                return EMatchType.NONE

    def toJava(self, val):

        from .._jclass import MetaJavaClass, JavaClass, JavaObject, JavaException
        from .._jproxy import PythonJavaClass
        from .._jvm    import get_jenv

        jenv = get_jenv()

        obj_classname = self._jclass[1:-1].replace("/", ".")

        if val is None:
            return None
        elif isinstance(val, str_types) and obj_classname in ("java.lang.String",
                                                              "java.lang.CharSequence",
                                                              "java.lang.Object"):
            from ...jvm.jframe import JFrame
            from .._conversion import convert_python_to_jstring
            with JFrame(jenv, 1):
                jstr = convert_python_to_jstring(val, jenv=jenv)
                return self._jt_jvm.JObject(jenv, jstr) if jstr else None
        elif isinstance(val, int_types) and obj_classname in ("java.lang.Integer",
                                                              "java.lang.Number",
                                                              "java.lang.Object"):
            return self._jt_jvm.JObject.newInteger(val)
        elif isinstance(val, int_types) and obj_classname in ("java.lang.Long",):
            return self._jt_jvm.JObject.newLong(val)
        elif isinstance(val, float) and obj_classname in ("java.lang.Float",):
            return self._jt_jvm.JObject.newFloat(val)
        elif isinstance(val, float) and obj_classname in ("java.lang.Double",):
            return self._jt_jvm.JObject.newDouble(val)
        elif isinstance(val, JavaClass):
            from .._conversion import _check_assignable_from
            _check_assignable_from(obj_classname, val)
            jc = val  # JavaClass
            return self._jt_jvm.JObject(jenv, jc.j_self.handle) if jc.j_self.handle else None
        elif isinstance(val, JavaObject):
            return self._jt_jvm.JObject(jenv, val.handle) if val.handle else None
        elif isinstance(val, MetaJavaClass):
            return self._jt_jvm.JObject(jenv, val._jclass.handle) if val._jclass.handle else None
        elif isinstance(val, PythonJavaClass):
            # from python class, get the proxy/python class
            if val.j_self is None: val._init_j_self_ptr()
            jc = val.j_self  # JavaClass
            return self._jt_jvm.JObject(jenv, jc.j_self.handle) if jc.j_self.handle else None
        elif isinstance(val, type):
            return self._jt_jvm.JObject(jenv, val.jcls) if val.jcls else None
        elif isinstance(val, (tuple, list)):
            from .._conversion import convert_python_to_jarray
            return convert_python_to_jarray(self._jclass, val, jenv=jenv)
        raise JavaException("Invalid python object for this argument. "
                            "Want {!r}, got {!r}".format(obj_classname, val))

    def toPython(self, val):

        with JVM.jvm as (_, jenv):
            return JString(jenv, val, own=False).str if val else None

    def setArgument(self, pdescr, args, pos, val):

        from .._jclass import MetaJavaClass, JavaClass, JavaObject, JavaException
        from .._jproxy import PythonJavaClass
        from .._jvm    import get_jenv

        jenv = get_jenv()

        obj_classname = self._jclass[1:-1].replace("/", ".")

        if val is None:
            val = None
        elif isinstance(val, str_types) and obj_classname in ("java.lang.String",
                                                              "java.lang.CharSequence",
                                                              "java.lang.Object"):
            from ...jvm.jframe import JFrame
            from .._conversion import convert_python_to_jstring
            with JFrame(jenv, 1):
                jstr = convert_python_to_jstring(val, jenv=jenv)
                val = self._jt_jvm.JObject(jenv, jstr) if jstr else None
        elif isinstance(val, JavaClass):
            from .._conversion import _check_assignable_from
            _check_assignable_from(obj_classname, val)
            jc = val  # JavaClass
            val = self._jt_jvm.JObject(jenv, jc.j_self.handle) if jc.j_self.handle else None
        elif isinstance(val, JavaObject):
            val = self._jt_jvm.JObject(jenv, val.handle) if val.handle else None
        elif isinstance(val, MetaJavaClass):
            val = self._jt_jvm.JObject(jenv, val._jclass.handle) if val._jclass.handle else None
        elif isinstance(val, PythonJavaClass):
            # from python class, get the proxy/python class
            if val.j_self is None: val._init_j_self_ptr()
            jc = val.j_self  # JavaClass
            val = self._jt_jvm.JObject(jenv, jc.j_self.handle) if jc.j_self.handle else None
        elif isinstance(val, type):
            val = self._jt_jvm.JObject(jenv, val.jcls) if val.jcls else None
        elif isinstance(val, (tuple, list)):
            from .._conversion import convert_python_to_jarray
            val = convert_python_to_jarray(self._jclass, val, jenv=jenv)
        else:
            raise JavaException("Invalid python object for this argument. "
                                "Want {!r}, got {!r}".format(obj_classname, val))
        args.setObject(pos, val)
