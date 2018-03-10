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
    - Has zero or more callees: functions/callables wired to it.
    - Each callee has optional wire-time arguments.
    - Calling it calls all wired callees , passing them any
      arguments given to call combined with the wire-time callee arguments.
    """

    def __init__(self, wiring_instance):

        self._wiring_instance = wiring_instance

        # Default min/max_callees to our instance's.
        self._min_callees = wiring_instance.min_callees
        self._max_callees = wiring_instance.max_callees

        # Wired (<callee>, <wire-time-args>, <wire-time-kwargs>) tuples.
        self._callees = []


    @property
    def min_callees(self):
        """
        Minimum number of allowed wirings. None means no limit.
        """
        return self._min_callees


    @min_callees.setter
    def min_callees(self, value):
        """
        Minimum number of allowed wirings. None means no limit. Must be:
        - A positive integer.
        - Less than or equal to max_callees
        - Less than or equal to the current number of wirings, if any.
        """
        if value is not None:
            callee_count = len(self._callees)
            if value <= 0:
                raise ValueError('min_callees must be positive or None')
            elif self._max_callees is not None and value > self._max_callees:
                raise ValueError('min_callees must be <= max_callees')
            elif callee_count and value > callee_count:
                raise ValueError('too few wired callees')

        self._min_callees = value


    @property
    def max_callees(self):
        """
        Maximum number of allowed wirings. None means no limit.
        """
        return self._max_callees


    @max_callees.setter
    def max_callees(self, value):
        """
        Maximum number of allowed wirings. None means no limit. Must be:
        - A positive integer.
        - Greater than or equal to min_callees
        - Greater than or equal to the current number of wirings, if any.
        """
        if value is not None:
            callee_count = len(self._callees)
            if value <= 0:
                raise ValueError('max_callees must be positive or None')
            elif self._min_callees is not None and value < self._min_callees:
                raise ValueError('max_callees must be >= min_callees')
            elif callee_count and value < callee_count:
                raise ValueError('too many wired callees')

        self._max_callees = value


    def wire(self, function, *args, **kwargs):

        """
        Wires `function` as a callee.

        `args` and `kwargs` are used to set wire-time arguments.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # self._max_callees can be None, meaning "no limit": comparison ok
        if len(self._callees) == self._max_callees:
            raise RuntimeError('max_callees limit reached')

        self._callees.append((function, args, kwargs))


    def unwire(self, function):

        """
        Unwires `function` as a callee.
        If `function` is wired multiple times, just unwires the first wiring.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # self._min_callees can be None, meaning "no limit": comparison ok
        if len(self._callees) == self._min_callees:
            raise RuntimeError('min_callees limit reached')

        tuples_to_remove = [v for v in self._callees if v[0] == function]
        if not tuples_to_remove:
            raise ValueError('unknown function %r' % (function,))
        self._callees.remove(tuples_to_remove[0])


    @staticmethod
    def calls_to(*_args, **_kwargs):

        """
        Called outside of a wiring action context, which makes no sense, as in
        `WiringShell.<callable>.calls_to(...)`.
        """

        raise RuntimeError('undefined wiring context')


    def __call__(self, *args, **kwargs):

        # Calling with wired callee count < `min_callees`, if set, is an error.
        min_callees = self._min_callees
        if min_callees and len(self._callees) < min_callees:
            raise RuntimeError('less than min_callees wired')

        # Get call coupling behaviour for this call from our WiringInstance and
        # then reset it to its default value to account for correct "default"
        # vs "overridden" call coupling behaviour.
        call_coupling = self._wiring_instance.coupling
        self._wiring_instance.coupling_reset()

        # Will contain (<exception>, <result>) per-callee tuples.
        call_result = []

        for callee, wire_args, wire_kwargs in self._callees:
            try:
                combined_args = list(wire_args)
                combined_args.extend(args)
                combined_kwargs = dict(wire_kwargs)
                combined_kwargs.update(kwargs)
                result = callee(*combined_args, **combined_kwargs)
                call_result.append((None, result))
            except Exception as e:
                call_result.append((e, None))
                if call_coupling:
                    raise RuntimeError(*call_result)

        return call_result


# ----------------------------------------------------------------------------
