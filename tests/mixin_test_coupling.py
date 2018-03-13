# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Caller/callee coupling test driver mixin.
"""


from __future__ import absolute_import

from wires import Wiring

from . import helpers



class WireAssertCouplingTestMixin(object):

    """
    Wiring and Assertion mixin for coupling tests.
    """

    EXCEPTION = ValueError('test exception message')

    return_42 = helpers.CallTracker(returns=42)
    return_none = helpers.CallTracker(returns=None)
    raise_exception = helpers.CallTracker(raises=EXCEPTION)



class TestCouplingMixin(WireAssertCouplingTestMixin):

    """
    Drives Wires call coupling tests.
    """

    # Tests added via generate_tests, below.



def _create_test_method(wiring_args, wire, ctao, raises, result, call_counts):

    def call_coupling_test_method(self):
        if wiring_args:
            self.w = Wiring(**wiring_args)
        for call_tracker in wire:
            call_tracker.reset()
            self.w.this.wire(call_tracker)
            self.addCleanup(self.w.this.unwire, call_tracker)
        if raises:
            with self.assertRaises(raises) as cm:
                self.w(**ctao).this()
            actual_result = cm.exception.args
        else:
            actual_result = self.w(**ctao).this()
        actual_call_counts = [w.call_count for w in wire]
        self.assertEqual(call_counts, actual_call_counts, 'call count mismatch')
        self.assertEqual(result, actual_result, 'result mismatch')

    return call_coupling_test_method



def _dict_to_method_name_part(arg_dict):

    return '_'.join('%s_%s' % (k, v) for k, v in arg_dict.items())



def _test_name(wiring_args, ctao, call):

    return 'test_wa_%s_ctao_%s_%s' % (
        _dict_to_method_name_part(wiring_args),
        _dict_to_method_name_part(ctao),
        call,
    )



def _generate_returns_42_test(test_class, wiring_args, ctao, returns):

    wire = [test_class.return_42]
    raises = None
    result = [(None, 42)] if returns else None
    call_counts = [1]

    setattr(
        test_class,
        _test_name(wiring_args, ctao, 'returns_42'),
        _create_test_method(wiring_args, wire, ctao, raises, result, call_counts),
    )


def _generate_raises_exc_test(test_class, wiring_args, ctao, returns):

    wire = [test_class.raise_exception]
    raises = None
    result = [(test_class.EXCEPTION, None)] if returns else None
    call_counts = [1]

    setattr(
        test_class,
        _test_name(wiring_args, ctao, 'raises_exception'),
        _create_test_method(wiring_args, wire, ctao, raises, result, call_counts),
    )


def _generate_2in3_raises_test(test_class, wiring_args, ctao, returns):

    wire = [
        test_class.return_42,
        test_class.raise_exception,
        test_class.return_none,
    ]
    raises = None
    if returns:
        result = [(None, 42), (test_class.EXCEPTION, None), (None, None)]
    else:
        result = None
    call_counts = [1, 1, 1]

    setattr(
        test_class,
        _test_name(wiring_args, ctao, '2in3_raises_exception'),
        _create_test_method(wiring_args, wire, ctao, raises, result, call_counts)
    )



def generate_tests(test_class, wiring_args_filter=None):
    """
    Creates test methods on `test_class` having a `TESTS` test description list.
    Entries in such list have two keys:
    - `wiring_args_filter`: Wiring initialization arguments for the associated `tests`.
    - `tests`: List of test specifications.
    Tests will only be created for matching wiring arguments.
    """
    call_coupling_arg_combinations = [
        {},
        {'returns': False},
        {'returns': True},
        # {'ignore_failures': False},
        # {'ignore_failures': True},
        # {'returns': False, 'ignore_failures': False},
        # {'returns': False, 'ignore_failures': True},
        # {'returns': True, 'ignore_failures': False},
        # {'returns': True, 'ignore_failures': True},
    ]
    for wiring_args in call_coupling_arg_combinations:
        if wiring_args_filter is None:
            if wiring_args:
                # no wiring_args_filter: skip test sets with wiring args.
                continue
        else:
            skip = False
            for arg, value in wiring_args_filter.items():
                if wiring_args.get(arg) != value:
                    # skip test sets with differet wiring args
                    skip = True
                    break
            if skip:
                continue
        # create the test methods
        for ctao in call_coupling_arg_combinations:
            returns = ctao.get('returns', wiring_args.get('returns', False))
            _generate_returns_42_test(test_class, wiring_args, ctao, returns)
            _generate_raises_exc_test(test_class, wiring_args, ctao, returns)
            _generate_2in3_raises_test(test_class, wiring_args, ctao, returns)


generate_tests(TestCouplingMixin)


# ----------------------------------------------------------------------------
