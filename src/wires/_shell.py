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
    # Holds the default per callable `min_wirings` and `max_wirings` as well
    # as the default caller/callee `coupling` mode:
    # - `min_wirings` and `max_wirings` are used by the instance at wire-time.
    # - `coupling` mode is used by the instance at call-time and can be
    #   overridden (again, at call-time), via `couple` / `decouple`.

    def __init__(self, min_wirings=None, max_wirings=None, coupling=False):

        if min_wirings is not None and min_wirings <= 0:
            raise ValueError('min_wirings must be positive or None')
        if max_wirings is not None and max_wirings <= 0:
            raise ValueError('max_wirings must be positive or None')
        if min_wirings and max_wirings and min_wirings > max_wirings:
            raise ValueError('max_wirings must be >= min_wirings')

        self._min_wirings = min_wirings
        self._max_wirings = max_wirings
        self._coupling = coupling
        self._wiring_instance = _instance.WiringInstance(self)


    @property
    def min_wirings(self):
        """
        Read-only default minimum wired callables.
        """
        return self._min_wirings


    @property
    def max_wirings(self):
        """
        Read-only default maximum wired callables.
        """
        return self._max_wirings


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
