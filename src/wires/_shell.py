# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wiring Shell.
"""

from __future__ import absolute_import

from . import _instance



class WiringShell(object):

    """
    Python Wiring Shell
    """

    # Wraps a Wiring Instance, cooperating with it by setting its
    # `wire_context` attribute to support the defined usage as in:
    #
    # >>> ws = WiringShell()
    # >>> ws.wire.some_callable.calls_to(<callee>)
    # >>> ws.unwire.some_callable.calls_to(<callee>)
    #
    # The `calls_to` method of the Wiring Callable wires/unwires the given
    # `<callee>` depending on its Wiring Instance `wire_context`, set by
    # the WiringShell object.

    def __init__(self):

        self._wiring = _instance.WiringInstance()


    @property
    def wire(self):
        """
        Callable/callee wiring attribute.
        """
        self._wiring._wire_context = True
        return self._wiring


    @property
    def unwire(self):
        """
        Callable/callee unwiring attribute.
        """
        self._wiring._wire_context = False
        return self._wiring


    @property
    def coupled_call(self):
        """
        """
        self._wiring._call_coupling = True
        return self._wiring


    @property
    def decoupled_call(self):
        """
        """
        self._wiring._call_coupling = False
        return self._wiring


    def __getattr__(self, name):

        return getattr(self._wiring, name)


# ----------------------------------------------------------------------------
