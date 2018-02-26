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

import logging
import sys
from traceback import print_exception



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

        # See `_log_handler_failure` below.
        self._use_log = True

        # Wired (callee, wire-time args, wire-time kwargs) tuples.
        self._functions = []


    @property
    def use_log(self):

        if self._wiring._wire_context is not None:
            raise RuntimeError('invalid access in wiring context')
        return self._use_log


    @use_log.setter
    def use_log(self, value):

        if self._wiring._wire_context is not None:
            raise RuntimeError('invalid access in wiring context')
        self._use_log = value


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
            self._functions.append((function, args, kwargs))
        elif wire_context is False:
            tuples_to_remove = [v for v in self._functions if v[0] == function]
            if not tuples_to_remove:
                raise ValueError('unknown function %r' % (function,))
            self._functions.remove(tuples_to_remove[0])
        else:
            raise RuntimeError('undefined wiring context')


    def __call__(self, *args, **kwargs):

        # Calls all callee functions.

        if self._wiring._wire_context is not None:
            raise RuntimeError('calling within wiring context')

        for function, wire_args, wire_kwargs in self._functions:
            try:
                combined_args = list(wire_args)
                combined_args.extend(args)
                combined_kwargs = dict(wire_kwargs)
                combined_kwargs.update(kwargs)
                function(*combined_args, **combined_kwargs)
            except Exception as e:
                # Catching exceptions here is critical to ensure decoupling
                # callables from callees.
                self._log_handler_failure(function, e)


    def _log_handler_failure(self, function, e):

        # Try to produce a useful message including:
        # - The callable name.
        # - The callee name.
        # - The raised execption.

        # `self.use_log` is used to prevent usage of the logging system:
        # necessary if any logging handler depends on calling us, which may
        # lead to us failing again, the handler failing again, ad infinitum
        #
        # Possible values:
        # - True: logging system will be used.
        # - False: outputs to sys.stderr.
        # - None: No output will be produced.
        #         (useful if logging system captures stderr)

        handler_name = self._handler_name(function)
        msg = '%r calling %r failed: %r' % (self._name, handler_name, e)
        if self.use_log:
            logger = logging.getLogger(self._logger_name)
            logger.error(msg)
            logger.exception(e)
        elif self.use_log is not None:
            sys.stderr.write(msg+'\n')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)


    @staticmethod
    def _handler_name(function):

        # Return the best possible name for the function.
        # Will be formatted like "module_name.function_name".

        function_name = getattr(function, '__qualname__', None)
        if function_name is None:
            # Older Python versions to not support __qualname__.
            function_name = getattr(function, '__name__', 'unnamed-callable')

        module_name = getattr(function, '__module__', 'unnamed-module')

        return '%s.%s' % (module_name, function_name)


# ----------------------------------------------------------------------------
