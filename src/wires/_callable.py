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
    Callable with a minimal API:

    - Has zero or more wirings: functions/callables wired to it.
    - Each wiring has optional wire-time arguments.
    - Calling it calls all wired functions/callables, passing them the
      combination of call-time and wire-time arguments.
    """

    def __init__(self, wiring, name, wiring_settings):

        self._wiring = wiring
        self._name = name

        # Default settings, from Wiring instance.
        self._wiring_settings = wiring_settings

        # Per callable settings.
        self._callable_settings = {}

        # Call-time settings.
        self._calltime_settings = {}

        # Wired (<callable>, <wire-time-args>, <wire-time-kwargs>) tuples.
        self._wirings = []


    def __repr__(self):

        return '<%s %r>' % (self.__class__.__name__, self._name)


    @property
    def __name__(self):
        """
        The callable name, like regular functions have.
        """
        return self._name


    # Used as a guard for non-set arguments in the `set` method call; `None`
    # would not be appropriate given than `min_wirings` and `max_wirings` take
    # `None` as valid value.

    not_set = object()

    def set(self, min_wirings=not_set, max_wirings=not_set, returns=not_set,
            ignore_failures=not_set, _next_call_only=False):
        """
        Sets one or more per-callable settings.

        The `not_set` defaults are used as a guard to identify non-set arguments.

        The `_next_call_only` argument is considered private and may be removed
        in future releases; it is used internally to override call-time settings.
        """

        if _next_call_only is True:
            target_settings = self._calltime_settings
        else:
            target_settings = self._callable_settings

        # Going with a `**kwargs` like argument would make this code simpler,
        # but the method signature would be more opaque; we prefer explicit
        # even though the code needs to repeat the argument names and work
        # at a somewhat "meta-ish" level.

        local_names = locals()
        arg_names = ('min_wirings', 'max_wirings', 'returns', 'ignore_failures')
        for name in arg_names:
            if local_names[name] is not self.not_set:
                target_settings[name] = local_names[name]


    @property
    def wirings(self):
        """
        List of wired (<callable>, <wire-time-args>, <wire-time-kwargs>) tuples,
        where <wire-time-args> is a tuple and <wire-time-kwargs> is a dict.
        """
        return list(self._wirings)


    def __len__(self):
        """
        Wiring count.
        """
        return len(self._wirings)


    def _effective_setting(self, setting_name):

        # Call-time settings take precedence over per-Callable settings, which
        # take precedence over Wiring settings.

        return self._calltime_settings.get(
            setting_name,
            self._callable_settings.get(
                setting_name,
                self._wiring_settings[setting_name]
            )
        )


    @property
    def min_wirings(self):
        """
        Minimum number of allowed wirings. None means no limit.
        """
        return self._effective_setting('min_wirings')


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
            elif self.max_wirings is not None and value > self.max_wirings:
                raise ValueError('min_wirings must be <= max_wirings')
            elif wiring_count and value > wiring_count:
                raise ValueError('too few wirings')

        self._callable_settings['min_wirings'] = value


    @property
    def max_wirings(self):
        """
        Maximum number of allowed wirings. None means no limit.
        """
        return self._effective_setting('max_wirings')


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
            elif self.min_wirings is not None and value < self.min_wirings:
                raise ValueError('max_wirings must be >= min_wirings')
            elif wiring_count and value < wiring_count:
                raise ValueError('too many wirings')

        self._callable_settings['max_wirings'] = value


    @property
    def returns(self):
        """
        If True, calling returns list of wired (<exception>, <result>) tuples.
        """
        return self._effective_setting('returns')


    @returns.setter
    def returns(self, value):

        self._callable_settings['returns'] = value


    @property
    def ignore_failures(self):
        """
        If False, stops calling wired callables on the first raised exception.
        """
        return self._effective_setting('ignore_failures')


    @ignore_failures.setter
    def ignore_failures(self, value):

        self._callable_settings['ignore_failures'] = value


    def __delattr__(self, name):
        """
        Removes any per-Callable setting, reverting to the Wiring instance's
        default values; raises ValueError if the resulting settings would be
        invalid.
        """
        # save and discard any current per-callable setting.
        try:
            save_value = self._callable_settings.pop(name)
        except KeyError:
            # not a local setting: fallback to super's __delattr__ and get out.
            super(WiringCallable, self).__delattr__(name)
            return

        # `next_value` would be effective after current value discarding; set
        # it, locally, to validate or trigger failures our setters have in place
        # (for example, can't set min_wirings to 3, with a single wiring).
        next_value = self._effective_setting(name)
        try:
            setattr(self, name, next_value)
        except ValueError:
            # `next_value` isn't valid, revert to `saved_value` and re-raise.
            setattr(self, name, save_value)
            raise

        # if we're here, `next_value` is valid: discard its local version.
        del self._callable_settings[name]


    def wire(self, function, *args, **kwargs):

        """
        Wires `function` with `args` and `kwargs` as wire-time arguments.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # self._max_wirings can be None, meaning "no limit": comparison ok
        if len(self._wirings) == self.max_wirings:
            raise RuntimeError('max_wirings limit reached')

        self._wirings.append((function, args, kwargs))


    def unwire(self, function):

        """
        Unwires `function`.
        If `function` is wired multiple times, just unwires the first wiring.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # self.min_wirings can be None, meaning "no limit": comparison ok
        if len(self._wirings) == self.min_wirings:
            raise RuntimeError('min_wirings limit reached')

        tuples_to_remove = [v for v in self._wirings if v[0] == function]
        if not tuples_to_remove:
            raise ValueError('unknown function %r' % (function,))
        self._wirings.remove(tuples_to_remove[0])


    def __call__(self, *args, **kwargs):

        # Calling with wiring count < `min_wirings`, if set, is an error.
        min_wirings = self.min_wirings
        if min_wirings and len(self._wirings) < min_wirings:
            raise RuntimeError('less than min_wirings wired')

        # Get call coupling behaviour for this call from our Wiring, resetting
        # it, to account for correct "default" vs "overridden" behaviour.
        return_or_raise = self.returns
        ignore_failures = self.ignore_failures
        self._calltime_settings.clear()

        # Will contain (<exception>, <result>) per-wiring tuples.
        call_result = []

        for wired_callable, wire_args, wire_kwargs in self._wirings:
            try:
                combined_args = list(wire_args)
                combined_args.extend(args)
                combined_kwargs = dict(wire_kwargs)
                combined_kwargs.update(kwargs)
                wired_result = wired_callable(*combined_args, **combined_kwargs)
                call_result.append((None, wired_result))
            except Exception as wired_exception:
                call_result.append((wired_exception, None))
                if not ignore_failures:
                    if return_or_raise:
                        raise RuntimeError(*call_result)
                    else:
                        break

        return call_result if return_or_raise else None


# ----------------------------------------------------------------------------
