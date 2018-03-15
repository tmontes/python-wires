# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wiring Instance.
"""

from __future__ import absolute_import

from . import _callable



class WiringInstance(object):

    """
    Python Wiring Instance
    """

    # Should be used wrapped in a Wires Shell.

    def __init__(self, wiring_shell):

        # Used to access the default call time coupling parameters.
        self._wiring_shell = wiring_shell

        # Tracks known Callable instances:
        # - Keys are callable names (this instance's dynamic attributes).
        # - Values are WiringCallable objects.
        self._wiring_callables = {}

        # Default call time coupling behavior is set by the shell, which will
        # be dynamically its `__call__` method which will set our `returns`
        # attribute; Wiring Callabls check this attribute to determine call
        # time coupling behaviour and *must* call our `coupling_reset` method
        # after that, to ensure correct "default" vs "overridde" behaviour.
        self.returns = wiring_shell.returns
        self.ignore_failures = wiring_shell.ignore_failures


    @property
    def min_wirings(self):
        """
        Read-only default minimum wired callables.
        """
        return self._wiring_shell.min_wirings


    @property
    def max_wirings(self):
        """
        Read-only default maximum wired callables.
        """
        return self._wiring_shell.max_wirings


    def coupling_reset(self):
        """
        Resets call time coupling behaviour to our shell's default.
        """
        self.returns = self._wiring_shell.returns
        self.ignore_failures = self._wiring_shell.ignore_failures


    def __getattr__(self, name):

        # Called on attribute access, returns an callable object.
        # Either uses a tracked one or creates new one, tracking it.

        try:
            return self._wiring_callables[name]
        except KeyError:
            new_callable = _callable.WiringCallable(self, name)
            self._wiring_callables[name] = new_callable
            return new_callable


    def __delattr__(self, name):

        # Deletes the tracked callable object.

        del self._wiring_callables[name]


    def __iter__(self):

        # Produces associated Callables.

        return iter(self._wiring_callables.values())


# ----------------------------------------------------------------------------
