# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wiring Callable.
"""

from __future__ import absolute_import



class WiringCallable(object):

    """
    Callable with a minimal API.
    Summary:
    - Has zero or more wirings: functions/callables wired to it.
    - Each wiring has optional wire-time arguments.
    - Calling it calls all wired functions/callables, passing them the
      combination of call-time and wire-time arguments.
    """

    def __init__(self, wiring_instance):

        self._wiring_instance = wiring_instance

        # Default min/max_wirings to our instance's.
        self._min_wirings = wiring_instance.min_wirings
        self._max_wirings = wiring_instance.max_wirings

        # Wired (<callable>, <wire-time-args>, <wire-time-kwargs>) tuples.
        self._wirings = []


    @property
    def min_wirings(self):
        """
        Minimum number of allowed wirings. None means no limit.
        """
        return self._min_wirings


    @min_wirings.setter
    def min_wirings(self, value):
        """
        Minimum number of allowed wirings. None means no limit. Must be:
        - A positive integer.
        - Less than or equal to max_wirings
        - Less than or equal to the current number of wirings, if any.
        """
        if value is not None:
            wiring_count = len(self._wirings)
            if value <= 0:
                raise ValueError('min_wirings must be positive or None')
            elif self._max_wirings is not None and value > self._max_wirings:
                raise ValueError('min_wirings must be <= max_wirings')
            elif wiring_count and value > wiring_count:
                raise ValueError('too few wirings')

        self._min_wirings = value


    @property
    def max_wirings(self):
        """
        Maximum number of allowed wirings. None means no limit.
        """
        return self._max_wirings


    @max_wirings.setter
    def max_wirings(self, value):
        """
        Maximum number of allowed wirings. None means no limit. Must be:
        - A positive integer.
        - Greater than or equal to min_wirings
        - Greater than or equal to the current number of wirings, if any.
        """
        if value is not None:
            wiring_count = len(self._wirings)
            if value <= 0:
                raise ValueError('max_wirings must be positive or None')
            elif self._min_wirings is not None and value < self._min_wirings:
                raise ValueError('max_wirings must be >= min_wirings')
            elif wiring_count and value < wiring_count:
                raise ValueError('too many wirings')

        self._max_wirings = value


    def wire(self, function, *args, **kwargs):

        """
        Wires `function` with `args` and `kwargs` as wire-time arguments.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # self._max_wirings can be None, meaning "no limit": comparison ok
        if len(self._wirings) == self._max_wirings:
            raise RuntimeError('max_wirings limit reached')

        self._wirings.append((function, args, kwargs))


    def unwire(self, function):

        """
        Unwires `function`.
        If `function` is wired multiple times, just unwires the first wiring.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # self._min_wirings can be None, meaning "no limit": comparison ok
        if len(self._wirings) == self._min_wirings:
            raise RuntimeError('min_wirings limit reached')

        tuples_to_remove = [v for v in self._wirings if v[0] == function]
        if not tuples_to_remove:
            raise ValueError('unknown function %r' % (function,))
        self._wirings.remove(tuples_to_remove[0])


    @staticmethod
    def calls_to(*_args, **_kwargs):

        """
        Called outside of a wiring action context, which makes no sense, as in
        `WiringShell.<callable>.calls_to(...)`.
        """

        raise RuntimeError('undefined wiring context')


    def __call__(self, *args, **kwargs):

        # Calling with wiring count < `min_wirings`, if set, is an error.
        min_wirings = self._min_wirings
        if min_wirings and len(self._wirings) < min_wirings:
            raise RuntimeError('less than min_wirings wired')

        # Get call coupling behaviour for this call from our WiringInstance and
        # then reset it to its default value to account for correct "default"
        # vs "overridden" call coupling behaviour.
        call_coupling = self._wiring_instance.coupling
        self._wiring_instance.coupling_reset()

        # Will contain (<exception>, <result>) per-wiring tuples.
        call_result = []

        for wired_callable, wire_args, wire_kwargs in self._wirings:
            try:
                combined_args = list(wire_args)
                combined_args.extend(args)
                combined_kwargs = dict(wire_kwargs)
                combined_kwargs.update(kwargs)
                result = wired_callable(*combined_args, **combined_kwargs)
                call_result.append((None, result))
            except Exception as e:
                call_result.append((e, None))
                if call_coupling:
                    raise RuntimeError(*call_result)

        return call_result


# ----------------------------------------------------------------------------
