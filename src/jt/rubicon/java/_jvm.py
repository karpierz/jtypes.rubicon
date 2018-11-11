# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib.compat import *
from ...jvm.lib import annotate, Optional
from ...jvm.lib import public
from ...jvm.lib import classproperty
from ...        import jni

from ...jvm import JVM as _JVM


@public
class JVM(_JVM):

    """Represents the Java virtual machine"""

    jvm  = classproperty(lambda cls: JVM._jvm)
    jenv = classproperty(lambda cls: JVM._jenv)

    _jvm  = None  # Optional[jt.jvm.JVM]
    _jenv = None  # Optional[jni.JNIEnv]

    def __init__(self, dll_path=None):

        from ._typemanager import TypeManager

        self._dll_path = None
        self._load(dll_path)
        self._create()
        self.type_manager = TypeManager()

    def __enter__(self):

        return self._jvm, JVM._jenv

    def start(self, *jvmoptions, **jvmargs):

        _, jenv = result = super(JVM, self).start(*jvmoptions, **jvmargs)
        JVM._jvm, JVM._jenv = self, jenv
        self._initialize(jenv)
        self.type_manager.start()
        return result

    def shutdown(self):

        self.type_manager.stop()
        _, jenv = self
        self._dispose(jenv)
        super(JVM, self).shutdown()
        JVM._jvm = JVM._jenv = None

    def _load(self, dll_path=None):

        from ...jvm.platform import JVMFinder
        from ...jvm          import EStatusCode

        if dll_path is not None:
            self._dll_path = dll_path

        if self._dll_path is None:
            finder = JVMFinder()
            self._dll_path = finder.get_jvm_path()

        super(JVM, self).__init__(self._dll_path)

    def _create(self):

        from .._java import jnirubicon
        self.ProxyHandler = jnirubicon.rubicon_reflect_ProxyHandler()
        self.Python       = jnirubicon.rubicon_Python()

    @annotate(jenv=jni.JNIEnv)
    def _initialize(self, jenv):

        self.ProxyHandler.initialize(jenv)
        self.Python.initialize(jenv)

    @annotate(jenv=jni.JNIEnv)
    def _dispose(self, jenv):

        self.ProxyHandler.dispose(jenv)
        self.Python.dispose(jenv)

    def handleException(self, exc):

        raise exc
