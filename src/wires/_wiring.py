# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires Wiring Class.

Wiring objects hold `WiringCallable`\ s: attributes that spring into existence
on first access.

>>> w = Wiring()
>>> c = w.one_callable      # Springs into existence.
>>> callable(c)             # Is callable.
True

`WiringCallable`\ s can then be called like regular functions:

>>> w.one_callable()        # Not wired, does nothing by default.

Wiring instances support introspection, via `dir` and `len`; iteration is also
supported:

>>> dir(w)                  # Get callable name list.
['one_callable']
>>> len(w)                  # How many callables in the instance?
1
>>> for c in w:            # Calling every callable in the instance.
...     c()

`WiringCallable`\ s can be deleted:

>>> del w.one_callable      # Delete and check it's gone.
>>> len(w)
0
"""

from __future__ import absolute_import

from . import _callable



class Wiring(object):

    """
    Wiring Class.
    """

    # Holds the default, per-callable, `min_wirings` and `max_wirings` as well
    # as the default caller/callee call coupling behaviour defining `returns`
    # and `ignore_failures` settings.
    #
    # Tracks wired callabes in `_callables` and call-time override settings in
    # `_calltime_settings`.

    def __init__(self, min_wirings=None, max_wirings=None, returns=False,
                 ignore_failures=True):
        """
        :param min_wirings: Minimum wirings that callables must have.
        :type min_wirings: Positive integer or None, for no minimum.

        :param max_wirings: Maximum wirings that callables can have.
        :type max_wirings: Positive integer or None, for no maximum.

        :param returns: Callables return/raise if `True`.
        :type returns: Boolean.

        :param ignore_failures: If `False`, all callables wired to our callables
                                will be called, in wiring order, regardless of
                                any of them raising exceptions. If `True`, wired
                                callable calling will stop after the first
                                exception.
        :type ignore_failures: Boolean.
        """
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


    def __getattr__(self, name):
        """
        Attribute based access to `WiringCallable`\ s.
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


    def __getitem__(self, name):
        """
        Index based access to `WiringCallable`\ s.
        """
        return self.__getattr__(name)


    def __delattr__(self, name):
        """
        Deletes `WiringCallable`\ s.
        """
        del self._callables[name]


    def __len__(self):
        """
        Existing `WiringCallable` count.
        """
        return len(self._callables)


    def __iter__(self):
        """
        Iterate over existing `WiringCallable`\ s.
        """
        return iter(self._callables.values())


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


# ----------------------------------------------------------------------------
