# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires :class:`Wiring` Class.

:class:`Wiring` objects hold callables as attributes that spring into existence
on first access; each such callable is a
:class:`WiringCallable <wires._callable.WiringCallable>` object.

>>> w = Wiring()
>>> c = w.one_callable      # Springs into existence.
>>> callable(c)             # Is callable.
True

Callables can also be accessed via indexing:

>>> w['one_callable'] is w.one_callable
True

:class:`Wiring` objects support :func:`dir`, :func:`len` and iteration:

>>> dir(w)                  # Get callable name list.
['one_callable']
>>> len(w)                  # How many callables?
1
>>> for c in w:             # Iterating over all callables.
...     print(c)
<WiringCallable 'one_callable'>


Deleting attributes deletes the associated callable:

>>> del w.one_callable      # Delete and check it's gone.
>>> len(w)
0
"""

from __future__ import absolute_import

from . import _callable



class Wiring(object):

    """
    :class:`Wiring` Class.
    """

    # Holds the default, per-callable, `min_wirings` and `max_wirings` as well
    # as the default caller/callee call-time coupling settings `returns` and
    # `ignore_exceptions` settings.
    #
    # Tracks wired callabes in `_callables` and call-time override settings in
    # `_calltime_settings`.

    def __init__(self, min_wirings=None, max_wirings=None, returns=False,
                 ignore_exceptions=True):
        """
        Initialization arguments determine default settings for this object's
        :class:`WiringCallable <wires._callable.WiringCallable>`\\s.

        Optional, per-:class:`WiringCallable <wires._callable.WiringCallable>`
        settings override these settings and, single use, call-time overriding
        is supported via calls to self: see :meth:`__call__`.

        :param min_wirings: Minimum wiring count.
        :type min_wirings: ``int`` > 0 or ``None``

        :param max_wirings: Maximum wiring count.
        :type max_wirings: ``int`` > 0 or ``None``

        :param returns: Calling returns results or raises exceptions if ``True``.
        :type returns: ``bool``

        :param ignore_exceptions: If ``True``, all wired callables will be
                                  called, regardless of raised exceptions;
                                  if ``False``, wired callable calling will stop
                                  after the first exception.
        :type ignore_exceptions: ``bool``
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
            'ignore_exceptions': ignore_exceptions,
        }

        # Tracks known Callable instances:
        # - Keys are callable names (this instance's dynamic attributes).
        # - Values are WiringCallable objects.
        self._callables = {}

        # Call time override settings.
        self._calltime_settings = {}


    def __repr__(self):
        """
        Evaluating creates a new object with the same initialization arguments.
        """
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join('%s=%r' % (k, v) for k, v in self._settings.items())
        )


    def __getattr__(self, name):
        """
        Attribute based access to :class:`WiringCallable <wires._callable.WiringCallable>`\\s.
        """
        try:
            the_callable = self._callables[name]
        except KeyError:
            new_callable = _callable.WiringCallable(
                _wiring=self,
                _name=name,
                _wiring_settings=self._settings,
            )
            self._callables[name] = new_callable
            the_callable = new_callable

        if self._calltime_settings:
            the_callable.set(_next_call_only=True, **self._calltime_settings)
            self._calltime_settings.clear()

        return the_callable


    def __getitem__(self, name):
        """
        Index based access to :class:`WiringCallable <wires._callable.WiringCallable>`\\s.
        """
        return self.__getattr__(name)


    def __delattr__(self, name):
        """
        Deletes :class:`WiringCallable <wires._callable.WiringCallable>`\\s
        or any other attributes.
        """
        try:
            del self._callables[name]
        except KeyError:
            super(Wiring, self).__delattr__(name)


    def __dir__(self):

        # Add our WiringCallable names to the attribute list.
        # Note: No super(...).__dir__() on Python 2!

        result = dir(super(Wiring, self))
        result.extend(self._callables.keys())
        result.extend(k for k in self.__dict__ if not k.startswith('_'))
        return result


    def __len__(self):
        """
        Existing :class:`WiringCallable <wires._callable.WiringCallable>` count.
        """
        return len(self._callables)


    def __iter__(self):
        """
        Iterate over existing :class:`WiringCallable <wires._callable.WiringCallable>`\\s.
        """
        return iter(self._callables.values())


    def __call__(self, returns=None, ignore_exceptions=None):
        """
        Call-time settings override.

        Usage example:

        >>> w = Wiring(returns=False)
        >>> w.one_callable()                # returns is False
        >>> w(returns=True).one_callable()  # returns is True for this call only
        []
        >>> w.one_callable()                # returns is still False
        """
        self._calltime_settings.clear()

        if returns is not None:
            self._calltime_settings['returns'] = returns
        if ignore_exceptions is not None:
            self._calltime_settings['ignore_exceptions'] = ignore_exceptions

        return self


# ----------------------------------------------------------------------------
