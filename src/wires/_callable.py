# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Simple callable.
"""


from __future__ import absolute_import

import logging
import sys
from traceback import print_exception



class Callable(object):

    """
    Callable with a minimal API.
    Summary:
    - Has zero or more handlers: functions/callables added to it.
    - Fired by calling it, like a function.
    - Firing it calls all associated handlers, passing them any
      arguments given to call.
    """

    def __init__(self, name, wires, logger_name='wires'):

        self._name = name
        self._wires = wires
        self._logger_name = logger_name

        # See `_log_handler_failure` below.
        self.use_log = True

        # Handler functions/callables.
        self._functions = []


    def calls_to(self, function):

        """
        Adds/removes `function` as a handler.
        """

        if not callable(function):
            raise ValueError('argument not callable: %r' % (function,))

        # TODO: explain
        if self._wires.wire_context:
            self._functions.append(function)
        else:
            try:
                self._functions.remove(function)
            except ValueError as e:
                e.args = ('unknown function %r: %s' % (function, e),)
                raise


    def __call__(self, *args, **kwargs):

        # Calls all handler functions.

        for function in self._functions:
            try:
                function(*args, **kwargs)
            except Exception as e:
                # Catching exceptions here is critical to ensure decoupling
                # callables from callees.
                self._log_handler_failure(function, e)


    def _log_handler_failure(self, function, e):

        # Try to produce a useful message including:
        # - The callable name.
        # - The function name.
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
            print_exception(type(e), e, e.__traceback__, file=sys.stderr)


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
