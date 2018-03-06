# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires Callable.
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

    def __init__(self, name, wiring, logger_name='wires'):

        self._name = name
        self._wiring = wiring
        self._logger_name = logger_name

        # Wired (callee, wire-time args, wire-time kwargs) tuples.
        self._callees = []


    def calls_to(self, function, *args, **kwargs):

        """
        Wires/unwires `function` as a callee.

        `args` and `kwargs` are used to set wire-time arguments and ignored
        when unwiring.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # Wire/unwire depending on our wiring `_wire_context` attribute.
        wire_context = self._wiring._wire_context
        self._wiring._wire_context = None

        if wire_context is True:
            self._callees.append((function, args, kwargs))
        elif wire_context is False:
            tuples_to_remove = [v for v in self._callees if v[0] == function]
            if not tuples_to_remove:
                raise ValueError('unknown function %r' % (function,))
            self._callees.remove(tuples_to_remove[0])
        else:
            raise RuntimeError('undefined wiring context')


    def __call__(self, *args, **kwargs):

        # Calls all callee functions.

        if self._wiring._wire_context is not None:
            raise RuntimeError('calling within wiring context')

        # Get call coupling behaviour for this call from our WiringInstance and
        # then reset it to its default value to account for correct "default"
        # vs "overridden" call coupling behaviour.
        call_coupling = self._wiring.coupling
        self._wiring.coupling_reset()

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
