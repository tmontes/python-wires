# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Caller/callee call time coupling test driver mixin.
"""


from __future__ import absolute_import

from wires import Wiring

from . import mixin_test_callables



# Overview
# --------
# Caller/callee call time coupling behaviour is defined by two boolean
# parameters: `returns` and `ignore_failures`.
#
# Depending on their values, call time behaviour is:
#
#                | ignore_failures=False       | ignore_failures=True
# ---------------+-----------------------------+------------------------------
# returns=False  | All wired callables are     | Stops calling wired callables
#                | called.                     | after first exception.
#                | Returns None.               | Returns None
# ---------------+-----------------------------+------------------------------
# returns=True   | All wired callables are     | Stops calling wired callables
#                | called.                     | after first exception.
#                | Returns list of (<e>, <r>)  | On wired callable exceptions
#                | tuples, one per wired       | raises `RuntimeError` with a
#                | callable.                   | list of (<e>, <r>) as arg;
#                |                             | otherwise, returns list of
#                |                             | (<e>, <r>) tuples, one per
#                |                             | wired callable.
# ----------------------------------------------------------------------------
#
#
# Usage
# -----
# The call time coupling parameters can be used at two levels:
#
# 1. When initializng a `Wiring` instance, via its initializer arguments:
#
#    >>> w = Wiring(returns=<bool>, ignore_failures=<bool>)
#
# 2. At call time, overriding the instance's default behaviour:
#
#    >>> w(returns=<bool>, ignore_failures=<bool>).some_callable()
#
#
# About the tests
# ---------------
# Testing combinations of initialization time coupling arguments vs. call time
# overriding arguments vs. single-/multi-/failing-/non-failing- wirings is non
# trivial and quickly leads to a combinatorial explosion.
#
# For that reason, call coupling tests are generated/synthesized instead of
# individually hand coded.
#
# The base idea is to run three test cases on every possible scenario:
#
# Case #1 - Wires a single callable that returns 42.
# Case #2 - Wires a single callable that raises a known exception.
# Case #3 - Wires three callables:
#           - The first returns 42.
#           - The second raises a known exception.
#           - The third returns None.
#
# This module contains two sets of objects:
# - Functions that add combinations of the three-test-set to a given class.
# - A Mixin class used with the bundled shared Wiring instance tests as well
#   as with a non-customized Wiring instance (like most other test Mixins are
#   used).



def _create_test_method(wiring_args, wire, ctao, raises, result, call_counts):

    def call_coupling_test_method(self):
        """
        Generic test method, covering all possible combinations.
        """

        # Replace the test class Wiring instance with a custom initialized one.
        if wiring_args:
            self.w = Wiring(**wiring_args)

        # Wire all wirings in `wire`, assumed to be helpers.CallTrackers.
        for call_tracker in wire:
            call_tracker.reset()
            self.w.this.wire(call_tracker)
            self.addCleanup(self.w.this.unwire, call_tracker)

        # Do the actual call with call-time argument overriding.
        if raises:
            with self.assertRaises(raises) as cm:
                self.w(**ctao).this()
            actual_result = cm.exception.args
        else:
            actual_result = self.w(**ctao).this()

        # Assert expected call counts.
        actual_call_counts = [w.call_count for w in wire]
        self.assertEqual(call_counts, actual_call_counts, 'call count mismatch')

        # Assert expected result.
        self.assertEqual(result, actual_result, 'result mismatch')

    return call_coupling_test_method



def _test_method_name(wa, ctao, call):

    # Test method names include instantiation-time argument names and values,
    # as well as call-time override argument names and values.

    def _dict_to_method_name_part(arg_dict):
        return '_'.join('%s_%s' % (k, v) for k, v in arg_dict.items())

    return 'test_wa_%s_ctao_%s_%s' % (
        _dict_to_method_name_part(wa),
        _dict_to_method_name_part(ctao),
        call,
    )



def _effective_returns(wa, ctao):

    # Return the effective value of `returns` based on instantiation time
    # argument dict `wa` and call time override dict `ctao`, considering that
    # the default instantiation time value is `False`.

    return ctao.get('returns', wa.get('returns', False))



def _effective_ignore_failures(wa, ctao):

    # Return the effective value of `ingore_failures` based on instantiation
    # time argument dict `wa` and call time override dict `ctao`, considering
    # that the default instantiation time value is `True`.

    return ctao.get('ignore_failures', wa.get('ignore_failures', True))



def _create_returns_42_test(test_class, wa, ctao):

    # Adds the first test case to `test_class`.
    # - `wa`: instance initialization arguments.
    # - `ctao`: call time argument overrides.

    # The effective `returns` value.
    returns = _effective_returns(wa, ctao)

    # Expected `result` depends on `returns`; everything else is constant.
    wire = [test_class.returns_42]
    raises = None
    result = [(None, 42)] if returns else None
    call_counts = [1]

    # Create and add the test to the class.
    setattr(
        test_class,
        _test_method_name(wa, ctao, 'case1_returns_42'),
        _create_test_method(wa, wire, ctao, raises, result, call_counts),
    )



def _create_raises_exc_test(test_class, wa, ctao):

    # Adds the second test case to `test_class`.
    # - `wa`: instance initialization arguments.
    # - `ctao`: call time argument overrides.

    # The effective `returns` and `ignore_failures` values.
    returns = _effective_returns(wa, ctao)
    ignore_failures = _effective_ignore_failures(wa, ctao)

    wire = [test_class.raises_exception]
    # Expected `result` and `raises` depend on `returns` and `ignore_failures`.
    if returns:
        if ignore_failures:
            result = [(test_class.EXCEPTION, None)] if returns else None
            raises = None
        else:
            # `raises` set to an Exception class, `result` is the expected
            # exception instance arguments: always a tuple.
            result = ((test_class.EXCEPTION, None),) if returns else None
            raises = RuntimeError
    else:
        result = None
        raises = None
    call_counts = [1]

    # Create and add the test to the class.
    setattr(
        test_class,
        _test_method_name(wa, ctao, 'case2_raises_exception'),
        _create_test_method(wa, wire, ctao, raises, result, call_counts),
    )



def _create_2in3_raises_test(test_class, wa, ctao):

    # Adds the thrid test case to `test_class`.
    # - `wa`: instance initialization arguments.
    # - `ctao`: call time argument overrides.

    # The effective `returns` and `ignore_failures` values.
    returns = _effective_returns(wa, ctao)
    ignore_failures = _effective_ignore_failures(wa, ctao)

    wire = [
        test_class.returns_42,
        test_class.raises_exception,
        test_class.returns_none,
    ]
    # Expected `result` and `raises` depend on `returns` and `ignore_failures`.
    if returns:
        if ignore_failures:
            result = [(None, 42), (test_class.EXCEPTION, None), (None, None)]
            raises = None
        else:
            result = ((None, 42), (test_class.EXCEPTION, None),)
            raises = RuntimeError
    else:
        result = None
        raises = None
    # Expected `call_counts` depend on `ignore_failures`.
    call_counts = [1, 1, 1] if ignore_failures else [1, 1, 0]

    # Create and add the test to the class.
    setattr(
        test_class,
        _test_method_name(wa, ctao, 'case3_2in3_raises_exception'),
        _create_test_method(wa, wire, ctao, raises, result, call_counts)
    )



CALL_COUPLING_ARG_COMBINATIONS = [
    # Purposely excluding the {} entry.
    {'returns': False},
    {'returns': True},
    {'ignore_failures': False},
    {'ignore_failures': True},
    {'returns': False, 'ignore_failures': False},
    {'returns': False, 'ignore_failures': True},
    {'returns': True, 'ignore_failures': False},
    {'returns': True, 'ignore_failures': True},
]



def generate_tests(test_class, wiring_args_filter=None):
    """
    Generates three test case set combinations and adds them to `test_class`.

    Considers all combinations of instantiation time and call time arguments in
    a combinatoric product, filtering out instantiation time combinations based
    on `wiring_args_filter`; this is used to target test generation to varying
    "starting points".

    Test case set combinations are then generated based on `wa` (instantiation
    time arguments) and `ctao` (call time argument overrides).
    """
    call_coupling_arg_combinations = [{}]
    call_coupling_arg_combinations.extend(CALL_COUPLING_ARG_COMBINATIONS)

    for wa in call_coupling_arg_combinations:
        if wiring_args_filter is None:
            if wa:
                # no wiring_args_filter: skip test sets with wiring args.
                continue
        else:
            skip = False
            for arg, value in wiring_args_filter.items():
                if wa.get(arg) != value:
                    # skip test sets with differet wiring args
                    skip = True
                    break
            if skip:
                continue
        # create the test methods
        for ctao in call_coupling_arg_combinations:
            _create_returns_42_test(test_class, wa, ctao)
            _create_raises_exc_test(test_class, wa, ctao)
            _create_2in3_raises_test(test_class, wa, ctao)



class TestCouplingMixin(mixin_test_callables.TestCallablesMixin):

    """
    Drives Wiring call coupling tests.
    """


# Generate tests, considering only default instantiation time arguments.

generate_tests(TestCouplingMixin, wiring_args_filter=None)


# ----------------------------------------------------------------------------
