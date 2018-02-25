# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires Shell.
"""

from __future__ import absolute_import

from . import _instance



class WiresShell(object):

    """
    Python Wires Shell
    """

    # Wraps a Wires Instance, cooperating with it by setting its
    # `wire_context` attribute to support the defined usage as in:
    #
    # >>> ws = WiresShell()
    # >>> ws.wire.some_callable.calls_to(<callee>)
    # >>> ws.unwire.some_callable.calls_to(<callee>)
    #
    # The `calls_to` method of the Wires Callable wires/unwires the given
    # `<callee>` depending on its Wires Instance `wire_context`, set by
    # the WiresShell object.

    def __init__(self):

        self._wires_instance = _instance.WiresInstance()


    @property
    def wire(self):
        """
        Callable/callee wiring attribute.
        """
        self._wires_instance._wire_context = True
        return self._wires_instance


    @property
    def unwire(self):
        """
        Callable/callee unwiring attribute.
        """
        self._wires_instance._wire_context = False
        return self._wires_instance


    def __getattr__(self, name):

        return getattr(self._wires_instance, name)


# ----------------------------------------------------------------------------
