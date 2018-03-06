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



class _ActionContext(object):

    """
    Supports `WiringShell.wire.<callable>` and `WiringShell.unwire.<callable>`
    wiring action contexts.
    """

    def __init__(self, wiring_callable):

        self._wiring_callable = wiring_callable


    def __call__(self, *args, **kwargs):

        raise RuntimeError('calling within wiring context')


class WiringActionContext(_ActionContext):

    """
    The `WiringShell.wire.<callable>` context.
    """

    def calls_to(self, function, *args, **kwargs):
        """
        Wiring action `WiringShell.wire.<callable>.calls_to(...)`.
        """
        return self._wiring_callable.wire(function, *args, **kwargs)



class UnwiringActionContext(_ActionContext):

    """
    The `WiringShell.unwire.<callable>` context.
    """

    def calls_to(self, function):
        """
        Unwiring action `WiringShell.unwire.<callable>.calls_to(...)`.
        """
        return self._wiring_callable.unwire(function)



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


    def wire(self, function, *args, **kwargs):

        """
        Wires `function` as a callee.

        `args` and `kwargs` are used to set wire-time arguments.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        self._callees.append((function, args, kwargs))


    def unwire(self, function):

        """
        Unwires `function` as a callee.
        If `function` is wired multiple times, just unwires the first wiring.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

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
