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

from . import _callable



class Wiring(object):

    """
    Python Wiring
    """

    # Holds the default, per-callable, `min_wirings` and `max_wirings` as well
    # as the default caller/callee call coupling behaviour defining `returns`
    # and `ignore_failures` settings.
    #
    # Tracks wired callabes in `_callables` and call-time override settings in
    # `_calltime_settings`.

    def __init__(self, min_wirings=None, max_wirings=None, returns=False,
                 ignore_failures=True):

        if min_wirings is not None and min_wirings <= 0:
            raise ValueError('min_wirings must be positive or None')
        if max_wirings is not None and max_wirings <= 0:
            raise ValueError('max_wirings must be positive or None')
        if min_wirings and max_wirings and min_wirings > max_wirings:
            raise ValueError('max_wirings must be >= min_wirings')

        self._settings = {
            # Default wiring limits.
            'min_wirings': min_wirings,
            'max_wirings': max_wirings,

            # Default call-time coupling behaviour.
            'returns': returns,
            'ignore_failures': ignore_failures,
        }

        # Tracks known Callable instances:
        # - Keys are callable names (this instance's dynamic attributes).
        # - Values are WiringCallable objects.
        self._callables = {}

        # Call time override settings.
        self._calltime_settings = {}


    def __repr__(self):

        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join('%s=%r' % (k, v) for k, v in self._settings.items())
        )


    def __call__(self, returns=None, ignore_failures=None):
        """
        Used for call-time parameter override.
        """
        self._calltime_settings.clear()

        if returns is not None:
            self._calltime_settings['returns'] = returns
        if ignore_failures is not None:
            self._calltime_settings['ignore_failures'] = ignore_failures

        return self


    def __getattr__(self, name):
        """
        Attribute based access to Callables.
        """
        try:
            the_callable = self._callables[name]
        except KeyError:
            new_callable = _callable.WiringCallable(self, name, self._settings)
            self._callables[name] = new_callable
            the_callable = new_callable

        if self._calltime_settings:
            the_callable.set(_next_call_only=True, **self._calltime_settings)
            self._calltime_settings.clear()

        return the_callable


    def __delattr__(self, name):
        """
        Deletes Callable attributes.
        """
        del self._callables[name]


    def __iter__(self):
        """
        Produces associated Callables.
        """
        return iter(self._callables.values())


    def __len__(self):
        """
        Callable count.
        """
        return len(self._callables)


    def __getitem__(self, name):
        """
        Index based access to Callables.
        """
        return self.__getattr__(name)


# ----------------------------------------------------------------------------
