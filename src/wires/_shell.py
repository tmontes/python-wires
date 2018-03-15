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

    # Holds the default, per-callable, `min_wirings` and `max_wirings` as well
    # as the default caller/callee call coupling behaviour defining `returns`
    # and `ignore_failures` settings.
    #
    # Wraps a Wiring Instance, cooperating with it by setting its `returns` and
    # `ignore_failures` attributes, to support call-time caller/callee coupling
    # behaviour overriding, while delegating attribute access to the wrapped
    # Wiring Instance to expose its behaviour.

    def __init__(self, min_wirings=None, max_wirings=None, returns=False,
                 ignore_failures=True):

        if min_wirings is not None and min_wirings <= 0:
            raise ValueError('min_wirings must be positive or None')
        if max_wirings is not None and max_wirings <= 0:
            raise ValueError('max_wirings must be positive or None')
        if min_wirings and max_wirings and min_wirings > max_wirings:
            raise ValueError('max_wirings must be >= min_wirings')

        self._min_wirings = min_wirings
        self._max_wirings = max_wirings
        self._returns = returns
        self._ignore_failures = ignore_failures
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
    def returns(self):
        """
        Read-only call coupling mode: calling returns values/raises exceptions?
        """
        return self._returns


    @property
    def ignore_failures(self):
        """
        Read-only call coupling mode: ignore callee exceptions?
        """
        return self._ignore_failures


    def __call__(self, returns=None, ignore_failures=None):
        """
        Used for call-time parameter override.
        """
        if returns is not None:
            self._wiring_instance.returns = returns
        if ignore_failures is not None:
            self._wiring_instance.ignore_failures = ignore_failures
        return self._wiring_instance


    def __getattr__(self, name):
        """
        Attribute based access to Callables.
        """
        return getattr(self._wiring_instance, name)


    def __delattr__(self, name):
        """
        Deletes Callable attributes.
        """
        delattr(self._wiring_instance, name)


    def __getitem__(self, name):
        """
        Index based access to Instance Callables.
        """
        return self.__getattr__(name)


# ----------------------------------------------------------------------------
