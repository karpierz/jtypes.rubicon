# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import

from ...... import jni
from ......jvm.jstring import JString


# Class: org.pybee.rubicon.Python

# Method: native static int start(String pythonHome, String pythonPath, String rubiconLib);

@jni.method("(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)I")
def start(env, cls,
          pythonHome, pythonPath, rubiconLib):

    # Start the Python runtime.

    jenv = env[0]

    ret = 0 # int

    """
    #ifdef LIBPYTHON_RTLD_GLOBAL
    #include <dlfcn.h>
    #endif

    char pythonPathVar[512];
    char rubiconLibVar[256];

    jenv = env;

    #ifdef LIBPYTHON_RTLD_GLOBAL
        // make libpython symbols availiable for everyone
        dlopen("libpython2.7.so", RTLD_LAZY|RTLD_GLOBAL|RTLD_NOLOAD);
    #endif

    // Special environment to prefer .pyo, and don't write bytecode if .py are found
    // because the process will not have write attribute on the device.
    putenv("PYTHONOPTIMIZE=2");
    putenv("PYTHONDONTWRITEBYTECODE=1");
    putenv("PYTHONNOUSERSITE=1");
    putenv("TARGET_ANDROID=1");

    if ( pythonHome )
        Py_SetPythonHome((char *)(*env)->GetStringUTFChars(env, pythonHome, NULL));

    if ( pythonPath )
    {
        sprintf(pythonPathVar, "PYTHONPATH=%s", (*env)->GetStringUTFChars(env, pythonPath, NULL));
        putenv(pythonPathVar);
    }

    #ifdef ANDROID
        // If we're on android, we need to specify the location of the Rubicon
        // shared library as part of the environment.
        if ( rubiconLib )
        {
            sprintf(rubiconLibVar, "RUBICON_LIBRARY=%s", (*env)->GetStringUTFChars(env, rubiconLib, NULL));
            putenv(rubiconLibVar);
        }
    #endif // ANDROID

    // putenv("PYTHONVERBOSE=1");

    Py_Initialize();
    // PySys_SetArgv(argc, argv);

    // If other modules are using threads, we need to initialize them before.
    PyEval_InitThreads();

    #ifdef ANDROID
        // Initialize and bootstrap the Android logging module
        initandroid();

        ret = PyRun_SimpleString(
            "import sys\n" \
            "import android\n" \
            "class LogFile(object):\n" \
            "    def __init__(self, level):\n" \
            "        self.buffer = ''\n" \
            "        self.level = level\n" \
            "    def write(self, s):\n" \
            "        s = self.buffer + s\n" \
            "        lines = s.split(\"\\n\")\n" \
            "        for line in lines[:-1]:\n" \
            "            self.level(line)\n" \
            "        self.buffer = lines[-1]\n" \
            "    def flush(self):\n" \
            "        return\n" \
            "sys.stdout = LogFile(android.info)\n" \
            "sys.stderr = LogFile(android.error)\n" \
            "print('Android Logging bootstrap active.')");
    #endif // ANDROID

    """
    return ret

# Method: native static void stop();

@jni.method("()V")
def stop(env, cls):

    # Stop the Python runtime.

    jenv = env[0]

    #if jenv:
    #    Py_Finalize();
    #    jenv = NULL;

# Method: native static int run(String script);

@jni.method("(Ljava/lang/String;)I")
def run(env, cls,
        script):

    # Method to run the Python script.

    jenv = env[0]

    filename = str(JString(jenv, script, own=False).str)

    try:
        script = open(filename, "r")
    except:
        return 1

    with script:
        #!!!return PyRun_SimpleFileEx(script, filename, 1)
        return 0

    """
    !!!from embed!!!
    try:
        script = open(filename, "rb")
    except:
        return throw_PyException(jenv, "Couldn't open script file.")

    with script:
        # check if it's a pyc/pyo file
        is_pyc_file = _maybe_pyc_file(script)
        if is_pyc_file:
            # Execute '.pyc' or '.pyo' file
            bcode = _read_pyc_bytecode(script)
            # Turn on optimization if a .pyo file is given
            ext = path.splitext(script.name)[1]
            Py_OptimizeFlag.value = (2 if ext == ".pyo" else 0)
        else:
            contents = script.read().decode()  # jaki encoding ???
            contents = "\n".join(contents.splitlines()).strip()  # trim \r\n, \r
            bcode = builtins.compile(contents, filename, "exec")

    scope = thread.globals
    try:
        exec(bcode, scope, scope)
    finally:
        if is_pyc_file:
            Py_OptimizeFlag.value = save_Py_OptimizeFlag
        # programs inside some java environments may get buffered output
        import sys
        sys.stdout.flush()
        sys.stderr.flush()
        sys.__stdout__.flush()
        sys.__stderr__.flush()

    """


__jnimethods__ = (
    start,
    stop,
    run,
)

__javacode__ = bytearray(  # Auto-generated; DO NOT EDIT!
    b"\xca\xfe\xba\xbe\x00\x00\x00\x34\x00\x10\x0a\x00\x03\x00\x0d\x07\x00\x0e\x07\x00"
    b"\x0f\x01\x00\x06\x3c\x69\x6e\x69\x74\x3e\x01\x00\x03\x28\x29\x56\x01\x00\x04\x43"
    b"\x6f\x64\x65\x01\x00\x05\x73\x74\x61\x72\x74\x01\x00\x39\x28\x4c\x6a\x61\x76\x61"
    b"\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x4c\x6a\x61\x76\x61\x2f\x6c"
    b"\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e"
    b"\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x29\x49\x01\x00\x03\x72\x75\x6e\x01\x00\x15"
    b"\x28\x4c\x6a\x61\x76\x61\x2f\x6c\x61\x6e\x67\x2f\x53\x74\x72\x69\x6e\x67\x3b\x29"
    b"\x49\x01\x00\x04\x73\x74\x6f\x70\x01\x00\x08\x3c\x63\x6c\x69\x6e\x69\x74\x3e\x0c"
    b"\x00\x04\x00\x05\x01\x00\x18\x6f\x72\x67\x2f\x70\x79\x62\x65\x65\x2f\x72\x75\x62"
    b"\x69\x63\x6f\x6e\x2f\x50\x79\x74\x68\x6f\x6e\x01\x00\x10\x6a\x61\x76\x61\x2f\x6c"
    b"\x61\x6e\x67\x2f\x4f\x62\x6a\x65\x63\x74\x00\x21\x00\x02\x00\x03\x00\x00\x00\x00"
    b"\x00\x05\x00\x01\x00\x04\x00\x05\x00\x01\x00\x06\x00\x00\x00\x11\x00\x01\x00\x01"
    b"\x00\x00\x00\x05\x2a\xb7\x00\x01\xb1\x00\x00\x00\x00\x01\x09\x00\x07\x00\x08\x00"
    b"\x00\x01\x09\x00\x09\x00\x0a\x00\x00\x01\x09\x00\x0b\x00\x05\x00\x00\x00\x08\x00"
    b"\x0c\x00\x05\x00\x01\x00\x06\x00\x00\x00\x0d\x00\x00\x00\x00\x00\x00\x00\x01\xb1"
    b"\x00\x00\x00\x00\x00\x00"
)
