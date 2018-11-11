# Copyright (c) 2016-2018, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from __future__ import absolute_import, print_function

import unittest
import sys
import os
import importlib
import logging

from . import test_dir

test_java = os.path.join(test_dir, "java")


def test_suite(names=None, omit=("run", "test_jni")):

    from . import __name__ as pkg_name
    from . import __path__ as pkg_path
    import unittest
    import pkgutil
    if names is None:
        names = [name for _, name, _ in pkgutil.iter_modules(pkg_path)
                 if name != "__main__" and name not in omit]
    names = [".".join((pkg_name, name)) for name in names]
    tests = unittest.defaultTestLoader.loadTestsFromNames(names)
    return tests


def main():

    sys.modules["rubicon"]      = importlib.import_module("jt.rubicon")
    sys.modules["rubicon.java"] = importlib.import_module("jt.rubicon.java")

    import jt.jvm.platform
    jvm_path = jt.jvm.platform.JVMFinder(java_version=1.8).get_jvm_path()

    print("Running testsuite using JVM:", jvm_path, "\n", file=sys.stderr)

    from jt.rubicon.java._jvm import JVM

    jvm = JVM(jvm_path)
    jvm.start("-Djava.class.path={}".format(
              os.pathsep.join([os.path.join(test_java, "classes")])),
              "-ea", "-Xms16M", "-Xmx512M")
    try:
        tests = test_suite(sys.argv[1:] or None)
        result = unittest.TextTestRunner(verbosity=2).run(tests)
    finally:
        jvm.shutdown()

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__.rpartition(".")[-1] == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)
    main()
