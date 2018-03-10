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

        # Needed to track parameters like `coupling`.
        self._wiring_shell = wiring_shell

        # Tracks known Callable instances:
        # - Keys are callable names (this instance's dynamic attributes).
        # - Values are WiringCallable objects.
        self._wiring_callables = {}

        # Call coupling behavior is set by the shell, which will be dynamically
        # overridden via its `couple` and `decouple` attributes, that set our
        # `coupled` attribute. Callables check this attribute to determine
        # call-time coupling and *must* call our `coupling_reset` after that
        # to ensure correct "default" vs "overridden" coupling.
        self.coupling = wiring_shell.coupling


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
        Resets call coupling behaviour to our shell's default.
        """
        self.coupling = self._wiring_shell.coupling


    def __getattr__(self, name):

        # Called on attribute access, returns an callable object.
        # Either uses a tracked one or creates new one, tracking it.

        try:
            return self._wiring_callables[name]
        except KeyError:
            new_callable = _callable.WiringCallable(self)
            self._wiring_callables[name] = new_callable
            return new_callable


# ----------------------------------------------------------------------------
