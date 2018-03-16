# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Caller/callee call-time coupling test driver mixin.
"""


from __future__ import absolute_import

from wires import Wiring

from . import mixin_test_callables



# Overview
# --------
# Caller/callee call-time coupling behaviour is defined by two boolean
# parameters: `returns` and `ignore_failures`.
#
# Depending on their values, call-time behaviour is:
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
# The call-time coupling parameters can be used at three levels:
#
# 1. When initializng a `Wiring` instance, via its initializer arguments:
#
#    >>> w = Wiring(returns=<bool>, ignore_failures=<bool>)
#
# 2. As a per-Callable setting:
#
#    >>> w.some_callable.returns = <bool>
#    >>> w.some_callable.ignore_failures = <bool>
#
# 3. At call-time, overriding the instance/callable's default behaviour:
#
#    >>> w(returns=<bool>, ignore_failures=<bool>).some_callable()
#
#
# About the tests
# ---------------
# Testing combinations of initialization-time coupling arguments vs. per-
# callable overriding arguments vs. call-time overriding arguments vs. single-/
# /multi-/failing-/non-failing- wirings is non trivial and quickly leads to a
# combinatorial explosion.
#
# For that reason, call coupling tests are generated/synthesized instead of
# individually hand coded.
#
# The base idea is to run two test cases on every possible scenario:
#
# Case #1 - Wires a single callable that returns 42.
# Case #2 - Wires three callables:
#           - The first returns None.
#           - The second raises a known exception.
#           - The third returns 42.
#
# This module contains two sets of objects:
# - Functions that add combinations of the two-test-set to a given class.
# - A Mixin class used with the bundled shared Wiring instance tests as well
#   as with a non-customized Wiring instance (like most other test Mixins are
#   used).



def _create_test_method(ita, wirings, pca, cta, raises, result, call_counts):

    def call_coupling_test_method(self):
        """
        Generic test method, covering all possible combinations.
        """

        # Replace the test class Wiring instance with a custom initialized one.
        if ita:
            self.w = Wiring(**ita)

        # Set per-callable settings.
        for callable_setting, callable_value in pca.items():
            setattr(self.w.this, callable_setting, callable_value)

        # Wire all wirings in `wire`, assumed to be helpers.CallTrackers.
        for call_tracker in wirings:
            call_tracker.reset()
            self.w.this.wire(call_tracker)
            self.addCleanup(self.w.this.unwire, call_tracker)

        # Do the actual call with call-time argument overriding.
        if raises:
            with self.assertRaises(raises) as cm:
                self.w(**cta).this()
            actual_result = cm.exception.args
        else:
            actual_result = self.w(**cta).this()

        # Assert expected call counts.
        actual_call_counts = [w.call_count for w in wirings]
        self.assertEqual(call_counts, actual_call_counts, 'call count mismatch')

        # Assert expected result.
        self.assertEqual(result, actual_result, 'result mismatch')

    return call_coupling_test_method



def _test_method_name(ita, pca, cta, call):

    # Test method names include instantiation-time argument names and values,
    # as well as per-callable arguments and call-time overriding argument names
    # and values.

    def _dict_to_method_name_part(arg_dict):
        return '_'.join('%s_%s' % (k, v) for k, v in arg_dict.items())

    return 'test_ita_%s_pca_%s_cta_%s_%s' % (
        _dict_to_method_name_part(ita),
        _dict_to_method_name_part(pca),
        _dict_to_method_name_part(cta),
        call,
    )



def _effective_returns(ita, pca, cta):

    # Return the effective value of `returns` based on instantiation-time
    # argument dict `ita`, per-callable argument dict `pca` and call-time
    # override dict `cta`, considering that the default, instantiation time,
    # value is `False`.

    return cta.get('returns', pca.get('returns', ita.get('returns', False)))



def _effective_ignore_failures(ita, pca, cta):

    # Return the effective value of `ignore_failures` based on instantiation-
    # time argument dict `ita`, per-callable argument dict `pca` and call-time
    # override dict `cta`, considering that the default, instantiation time,
    # value is `True`.

    return cta.get(
        'ignore_failures',
        pca.get('ignore_failures', ita.get('ignore_failures', True))
    )



def _create_returns_42_test(test_class, ita, pca, cta):

    # Adds the first test case to `test_class`.
    # - `ita`: instance initialization-time arguments.
    # - `pca`: per-callable arguments
    # - `cta`: call-time argument overrides.

    # The effective `returns` value.
    returns = _effective_returns(ita, pca, cta)

    # Expected `result` depends on `returns`; everything else is constant.
    wirings = [test_class.returns_42]
    raises = None
    result = [(None, 42)] if returns else None
    call_counts = [1]

    # Create and add the test to the class.
    setattr(
        test_class,
        _test_method_name(ita, pca, cta, 'case1_returns_42'),
        _create_test_method(ita, wirings, pca, cta, raises, result, call_counts)
    )



def _create_2in3_raises_test(test_class, ita, pca, cta):

    # Adds the thrid test case to `test_class`.
    # - `ita`: instance initialization-time arguments.
    # - `pca`: per-callable arguments
    # - `cta`: call-time argument overrides.

    # The effective `returns` and `ignore_failures` values.
    returns = _effective_returns(ita, pca, cta)
    ignore_failures = _effective_ignore_failures(ita, pca, cta)

    wirings = [
        test_class.returns_none,
        test_class.raises_exception,
        test_class.returns_42,
    ]
    # Expected `result` and `raises` depend on `returns` and `ignore_failures`.
    if returns:
        if ignore_failures:
            result = [(None, None), (test_class.EXCEPTION, None), (None, 42)]
            raises = None
        else:
            result = ((None, None), (test_class.EXCEPTION, None),)
            raises = RuntimeError
    else:
        result = None
        raises = None
    # Expected `call_counts` depend on `ignore_failures`.
    call_counts = [1, 1, 1] if ignore_failures else [1, 1, 0]

    # Create and add the test to the class.
    setattr(
        test_class,
        _test_method_name(ita, pca, cta, 'case3_2in3_raises_exception'),
        _create_test_method(ita, wirings, pca, cta, raises, result, call_counts)
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



def generate_tests(test_class, ita_filter=None):
    """
    Generates three test case set combinations and adds them to `test_class`.

    Considers all combinations of Wiring instantiation time, per-callable and
    call-time arguments in a combinatoric product, filtering out instantiation
    time combinations based on `ita_filter`; this is used to target test
    generation to varying "starting points".

    Test case set combinations are then generated based on `ita` (instantiation-
    time arguments), `pca` (per-callable arguments) and `cta` (call-time
    argument overrides).
    """
    call_coupling_arg_combinations = [{}]
    call_coupling_arg_combinations.extend(CALL_COUPLING_ARG_COMBINATIONS)

    for ita in call_coupling_arg_combinations:
        if ita_filter is None:
            if ita:
                # no ita_filter: skip test sets with wiring args.
                continue
        else:
            skip = False
            for arg, value in ita_filter.items():
                if ita.get(arg) != value:
                    # skip test sets with differet wiring args
                    skip = True
                    break
            if skip:
                continue
        # create the test methods
        for pca in call_coupling_arg_combinations:
            for cta in call_coupling_arg_combinations:
                _create_returns_42_test(test_class, ita, pca, cta)
                _create_2in3_raises_test(test_class, ita, pca, cta)



class TestCouplingMixin(mixin_test_callables.TestCallablesMixin):

    """
    Drives Wiring call coupling tests.
    """


# Generate tests, considering only default instantiation time arguments.

generate_tests(TestCouplingMixin, ita_filter=None)


# ----------------------------------------------------------------------------
