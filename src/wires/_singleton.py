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

    def __init__(self, wires_shell):
        self._wires_shell = wires_shell

    def __getitem__(self, name):
        return getattr(self, name)



class _WireWrapper(_Wrapper):

    def __getattr__(self, name):
        self._wires_shell._wires_instance._wire_context = True
        return getattr(self._wires_shell._wires_instance, name)



class _UnwireWrapper(_Wrapper):

    def __getattr__(self, name):
        self._wires_shell._wires_instance._wire_context = False
        return getattr(self._wires_shell._wires_instance, name)



class _WiresSingleton(object):

    def __init__(self):
        wires_shell = _shell.WiresShell()
        self.wire = _WireWrapper(wires_shell)
        self.unwire = _UnwireWrapper(wires_shell)



_WIRE_SINGLETON = _WiresSingleton()

wire = _WIRE_SINGLETON.wire
unwire = _WIRE_SINGLETON.unwire


# ----------------------------------------------------------------------------
