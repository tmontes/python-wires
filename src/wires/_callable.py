# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires :class:`WiringCallable` Class.

:class:`WiringCallable`\\s are callable objects used exclusively as
:class:`Wiring <wires._wiring.Wiring>` object attributes.

>>> w = Wiring()
>>> callable(w.one_callable)
True

Each :class:`WiringCallable` has zero or more wirings: functions/callables
wired to it. Their :meth:`wire <WiringCallable.wire>` method is used to add
wirings, including optional wire-time arguments:

>>> w.one_callable.wire(print, 'hi')    # Wire `print`: one wire-time positional arg.
>>> w.one_callable.wire(print, 'bye')   # 2nd `print` wiring: different wire-time arg.

Calling a :class:`WiringCallable` calls its wirings, in wiring order, passing
them a combination of the optional wire-time and optional call-time arguments:

>>> w.one_callable('world', end='!\\n') # Call with call-time positional and named args.
hi world!
bye world!

:class:`WiringCallable`\\s have a :attr:`wirings <WiringCallable.wirings>`
attribute, representing all current wirings, and include support for :func:`len`,
returning the wiring count:

>>> w.one_callable.wirings
[(<built-in function print>, ('hi',), {}), (<built-in function print>, ('bye',), {})]
>>> len(w.one_callable)
2

:class:`WiringCallable` objects behave differently depending on their
:class:`Wiring <wires._wiring.Wiring>` object's settings and on their own
:attr:`min_wirings <WiringCallable.min_wirings>`,
:attr:`max_wirings <WiringCallable.max_wirings>`,
:attr:`returns <WiringCallable.returns>` and
:attr:`ignore_failures <WiringCallable.ignore_failures>` attributes.
"""

from __future__ import absolute_import



class WiringCallable(object):

    """
    :class:`WiringCallable` Class.
    """

    def __init__(self, _wiring, _name, _wiring_settings):
        """
        **IMPORTANT**

        Do not instantiate :class:`WiringCallable` objects;
        :class:`Wiring <wires._wiring.Wiring>` objects do that, when needed. All
        initialization arguments are considered private and may change in future
        releases.
        """

        # _wiring - The `Wiring` object we're a part of.
        # _name - The attribute name in `_wiring` leading to us.
        # _wiring_settings - The default callable settings in `_wiring`;
        #                    passed because it's private to `Wiring` objects.

        self._wiring = _wiring
        self._name = _name

        # Default settings, from Wiring instance.
        self._wiring_settings = _wiring_settings

        # Per callable settings.
        self._callable_settings = {}

        # Call-time settings.
        self._calltime_settings = {}

        # Wired (<callable>, <wire-time-args>, <wire-time-kwargs>) tuples.
        self._wirings = []


    def __repr__(self):

        return '<%s %r at 0x%x>' % (self.__class__.__name__, self._name, id(self))


    @property
    def __name__(self):
        """
        The callable name, like regular functions have.
        """
        return self._name


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
        Minimum number of wirings or ``None``, meaning no limit.

        Reading returns the per-:class:`WiringCallable` value, if set, falling
        back to the containing :class:`Wiring <wires._wiring.Wiring>`'s setting.
        Writing assigns a per-:class:`WiringCallable` value that, if
        non-``None``, must be:

        - An ``int`` > 0.
        - Less than or equal to :attr:`max_wirings`.
        - Less than or equal to the wiring count, if there are wirings.

        :raises ValueError: When assigned invalid values.
        """
        return self._effective_setting('min_wirings')


    @min_wirings.setter
    def min_wirings(self, value):

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
        Maximum number of wirings or ``None``, meaning no limit.

        Reading returns the per-:class:`WiringCallable` value, if set, falling
        back to the containing :class:`Wiring <wires._wiring.Wiring>`'s setting.
        Writing assigns a per-:class:`WiringCallable` value that, if
        non-``None``, must be:

        - An ``int`` > 0.
        - Greater than or equal to :attr:`min_wirings`.
        - Greater than or equal to the wiring count, if there are wirings.

        :raises ValueError: When assigned non-conforming values.
        """
        return self._effective_setting('max_wirings')


    @max_wirings.setter
    def max_wirings(self, value):

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
        ``bool`` value defining call-time coupling behaviour: see :meth:`__call__`.

        Reading returns the per-:class:`WiringCallable` value, if set, falling
        back to the containing :class:`Wiring <wires._wiring.Wiring>`'s setting.
        Writing assigns a per-:class:`WiringCallable` value.
        """
        return self._effective_setting('returns')


    @returns.setter
    def returns(self, value):

        self._callable_settings['returns'] = value


    @property
    def ignore_failures(self):
        """
        ``bool`` value defining call-time coupling behaviour: see :meth:`__call__`.

        Reading returns the per-:class:`WiringCallable` value, if set, falling
        back to the containing :class:`Wiring <wires._wiring.Wiring>`'s setting.
        Writing assigns a per-:class:`WiringCallable` value.
        """
        return self._effective_setting('ignore_failures')


    @ignore_failures.setter
    def ignore_failures(self, value):

        self._callable_settings['ignore_failures'] = value


    # Used as a guard for non-set arguments in the `set` method call; `None`
    # would not be appropriate given than `min_wirings` and `max_wirings` take
    # `None` as valid value.

    _not_set = object()

    def set(self, min_wirings=_not_set, max_wirings=_not_set, returns=_not_set,
            ignore_failures=_not_set, _next_call_only=False):
        """
        Sets one or more per-:class:`WiringCallable` settings.

        :param min_wirings: See :attr:`min_wirings`.

        :param max_wirings: See :attr:`max_wirings`.

        :param returns: See :attr:`returns`.

        :param ignore_failures: See :attr:`ignore_failures`.

        :param _next_call_only: **IMPORTANT**: This argument is considered
                                private and may be changed or removed in future
                                releases.

        :raises: May raise exceptions. Refer to the per-attribute documentation.

        The uncommon defaults are used as a guard to identify non-set arguments,
        given than ``None`` is a valid value for ``min_wirings`` and ``max_wirings``.
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
            if local_names[name] is not self._not_set:
                target_settings[name] = local_names[name]


    def __delattr__(self, name):
        """
        Removes per-:class:`WiringCallable` settings.

        :param name: An existing attribute name.
        :type name:  ``str``

        :raises: May raise exceptions if the resulting settings would be invalid.
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
        Adds a new wiring to ``function``, with ``args`` and ``kwargs`` as
        wire-time arguments.

        :raises TypeError: If ``function`` is not :func:`callable`.
        :raises RuntimeError: If :attr:`max_wirings` would be violated.
        """
        if not callable(function):
            raise TypeError('argument not callable: %r' % (function,))

        # self._max_wirings can be None, meaning "no limit": comparison ok
        if len(self._wirings) == self.max_wirings:
            raise RuntimeError('max_wirings limit reached')

        self._wirings.append((function, args, kwargs))


    def unwire(self, function):
        """
        Removes the first wiring to ``function``.

        :raises TypeError: If ``function`` is not :func:`callable`.
        :raises ValueError: If ``function`` is not wired.
        :raises RuntimeError: If :attr:`min_wirings` would be violated.
        """
        if not callable(function):
            raise TypeError('argument not callable: %r' % (function,))

        # self.min_wirings can be None, meaning "no limit": comparison ok
        if len(self._wirings) == self.min_wirings:
            raise RuntimeError('min_wirings limit reached')

        tuples_to_remove = [v for v in self._wirings if v[0] == function]
        if not tuples_to_remove:
            raise ValueError('unknown function %r' % (function,))
        self._wirings.remove(tuples_to_remove[0])


    @property
    def wirings(self):
        """
        List of ``(<function>, <args>, <kwargs>)`` wiring tuples, in wiring
        order, where ``<args>`` and ``<kwargs>`` are the wire-time arguments
        passed to :meth:`wire`.
        """
        return list(self._wirings)


    def __call__(self, *args, **kwargs):
        """
        Calls wirings, in wiring order.

        :raises ValueError: If the wiring count is lower than
                            :attr:`min_wirings`, when set to an ``int`` > 0.

        Argument passing:

        * Wired functions are passed a combination of the wire-time and
          call-time arguments; wire-time positional arguments will be passed
          first, followed by the call-time ones; wire-time named arguments may
          be overridden by call-time ones.

        Call-time coupling. Depends on:

        * :attr:`returns`: if ``False``, calling returns ``None``; otherwise,
          returns or raises (see below).
        * :attr:`ignore_failures`: if ``False``, calling wirings stops on the
          first wiring-raised exception; otherwise, all wirings will be called.

        :returns: A list of ``(<exception>, <result>)`` tuples, in wiring order,
                  where: ``<exception>`` is ``None`` and ``<result>`` holds the
                  returned value from that wiring, if no exception was raised;
                  otherwise, ``<exception>`` is the raised exception and
                  ``<result>`` is ``None``.

        :raises RuntimeError: Only if :attr:`returns` is ``True``,
                              :attr:`ignore_failures` is ``False``, and a
                              wiring raises an exception. The exception
                              arguments will be a tuple of
                              ``(<exception>, <result>)`` tuples, much like the
                              returned ones, where only the last one will have
                              ``<exception>`` as a non-``None`` value.
        """

        # Calling with wiring count < `min_wirings`, if set, is an error.
        min_wirings = self.min_wirings
        if min_wirings and len(self._wirings) < min_wirings:
            raise ValueError('less than min_wirings wired')

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


    def __len__(self):
        """
        Wiring count.
        """
        return len(self._wirings)


# ----------------------------------------------------------------------------
