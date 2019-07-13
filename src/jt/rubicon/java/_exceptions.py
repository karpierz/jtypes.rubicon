# Copyright (c) 2016-2019, Adam Karpierz
# Licensed under the BSD license
# http://opensource.org/licenses/BSD-3-Clause

from ...jvm.lib import py2compatible
from ...jvm.lib import public


@public
@py2compatible
class UnknownClassException(Exception):

    def __init__(self, descriptor):
        self.descriptor = descriptor

    def __str__(self):
        return "Couldn't find Java class '{}'".format(self.descriptor)
