# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

from . import _shell



class _WireWrapper(object):

    def __init__(self, wires_shell):
        self._wires_shell = wires_shell

    def __getattr__(self, name):
        self._wires_shell._wires_instance.wire_context = True
        return getattr(self._wires_shell._wires_instance, name)



class _UnwireWrapper(object):

    def __init__(self, wires_shell):
        self._wires_shell = wires_shell

    def __getattr__(self, name):
        self._wires_shell._wires_instance.wire_context = False
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
