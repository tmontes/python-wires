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
    # Holds the default per callable `min_callee` and `max_callee` as well
    # as the default caller/callee `coupling` mode:
    # - `min_callee` and `max_callee` are used by the instance at wire-time.
    # - `coupling` mode is used by the instance at call-time and can be
    #   overridden (again, at call-time), via `couple` / `decouple`.

    def __init__(self, min_callees=None, max_callees=None, coupling=False):

        if min_callees is not None and min_callees <= 0:
            raise ValueError('min_callees must be positive or None')
        if max_callees is not None and max_callees <= 0:
            raise ValueError('max_callees must be positive or None')
        if min_callees and max_callees and min_callees > max_callees:
            raise ValueError('max_callees must be >= min_callees')

        self._min_callees = min_callees
        self._max_callees = max_callees
        self._coupling = coupling
        self._wiring_instance = _instance.WiringInstance(self)


    @property
    def min_callees(self):
        """
        Read-only default minimum wired callees.
        """
        return self._min_callees


    @property
    def max_callees(self):
        """
        Read-only default maximum wired callees.
        """
        return self._max_callees


    @property
    def coupling(self):
        """
        Read-only default call coupling mode.
        """
        return self._coupling


    @property
    def couple(self):
        """
        Caller/callee coupled call context attribute (overrides default).
        """
        self._wiring_instance.coupling = True
        return self._wiring_instance


    @property
    def decouple(self):
        """
        Caller/callee decoupled call context attribute (overrides default).
        """
        self._wiring_instance.coupling = False
        return self._wiring_instance


    def __getattr__(self, name):

        return getattr(self._wiring_instance, name)


    def __getitem__(self, name):

        return self.__getattr__(name)


# ----------------------------------------------------------------------------
