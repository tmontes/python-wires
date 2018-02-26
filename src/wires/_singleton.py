# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires Singleton.
"""

from __future__ import absolute_import

from . import _shell



class _Wrapper(object):

    def __init__(self, wiring_shell):
        self._wiring_shell = wiring_shell

    def __getitem__(self, name):
        return getattr(self, name)



class _WireWrapper(_Wrapper):

    def __getattr__(self, name):
        self._wiring_shell._wiring._wire_context = True
        return getattr(self._wiring_shell._wiring, name)



class _UnwireWrapper(_Wrapper):

    def __getattr__(self, name):
        self._wiring_shell._wiring._wire_context = False
        return getattr(self._wiring_shell._wiring, name)



class _WiresSingleton(object):

    def __init__(self):
        wiring_shell = _shell.WiringShell()
        self.wire = _WireWrapper(wiring_shell)
        self.unwire = _UnwireWrapper(wiring_shell)



_WIRE_SINGLETON = _WiresSingleton()

wire = _WIRE_SINGLETON.wire
unwire = _WIRE_SINGLETON.unwire


# ----------------------------------------------------------------------------
