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
    #
    # Also holds the default call `coupling` mode used by the Instance and
    # Callables to determine call-time behavior; the coupling mode can also
    # be overridden at call-time via `coupled_call` and `decoupled_call`.

    def __init__(self, coupling=False):

        self._coupling = coupling
        self._wiring_instance = _instance.WiringInstance(self)


    @property
    def coupling(self):
        """
        Read-only default call coupling mode.
        """
        return self._coupling


    @property
    def wire(self):
        """
        Callable/callee wiring context attribute.
        """
        return _instance.InstanceWiringActionContext(self._wiring_instance)


    @property
    def unwire(self):
        """
        Callable/callee unwiring context attribute.
        """
        return _instance.InstanceUnwiringActionContext(self._wiring_instance)


    @property
    def coupled_call(self):
        """
        Caller/callee coupled call context attribute (overrides default).
        """
        self._wiring_instance.coupling = True
        return self._wiring_instance


    @property
    def decoupled_call(self):
        """
        Caller/callee decoupled call context attribute (overrides default).
        """
        self._wiring_instance.coupling = False
        return self._wiring_instance


    def __getattr__(self, name):

        return getattr(self._wiring_instance, name)


# ----------------------------------------------------------------------------
