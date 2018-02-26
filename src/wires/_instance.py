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

    def __init__(self):

        # Tracks known Callable instances:
        # - Keys are callable names (my dynamic attributes).
        # - Values are Callable objects.

        self._callables = {}

        # Our callers' `calls_to` method checks this attribute to decide
        # whether to wire or unwire the passed in callee; also used to
        # disallow calling from within wiring/unwiring contexts.
        self._wire_context = None


    def __getattr__(self, name):

        # Called on attribute access, returns an callable object.
        # Either uses a tracked one or creates new one, tracking it.

        try:
            return self._callables[name]
        except KeyError:
            new_callable = _callable.WiringCallable(name, self)
            self._callables[name] = new_callable
            return new_callable


    def __getitem__(self, name):

        # Support attribute access for simpler dynamic name wiring/unwiring.

        return self.__getattr__(name)


# ----------------------------------------------------------------------------
