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



class TestCouplingMixin(mixin_test_callables.TestCallablesMixin):

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



def _test_name(wa, ctao, call):

    return 'test_wa_%s_ctao_%s_%s' % (
        _dict_to_method_name_part(wa),
        _dict_to_method_name_part(ctao),
        call,
    )



def _generate_returns_42_test(test_class, wa, ctao, returns, ignore_failures):

    wire = [test_class.returns_42]
    raises = None
    result = [(None, 42)] if returns else None
    call_counts = [1]

    setattr(
        test_class,
        _test_name(wa, ctao, 'returns_42'),
        _create_test_method(wa, wire, ctao, raises, result, call_counts),
    )


def _generate_raises_exc_test(test_class, wa, ctao, returns, ignore_failures):

    wire = [test_class.raises_exception]
    if returns:
        if ignore_failures:
            result = [(test_class.EXCEPTION, None)] if returns else None
            raises = None
        else:
            result = ((test_class.EXCEPTION, None),) if returns else None
            raises = RuntimeError
    else:
        result = None
        raises = None
    call_counts = [1]

    setattr(
        test_class,
        _test_name(wa, ctao, 'raises_exception'),
        _create_test_method(wa, wire, ctao, raises, result, call_counts),
    )


def _generate_2in3_raises_test(test_class, wa, ctao, returns, ignore_failures):

    wire = [
        test_class.returns_42,
        test_class.raises_exception,
        test_class.returns_none,
    ]
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
    call_counts = [1, 1, 1] if ignore_failures else [1, 1, 0]

    setattr(
        test_class,
        _test_name(wa, ctao, '2in3_raises_exception'),
        _create_test_method(wa, wire, ctao, raises, result, call_counts)
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
        {'ignore_failures': False},
        {'ignore_failures': True},
        {'returns': False, 'ignore_failures': False},
        {'returns': False, 'ignore_failures': True},
        {'returns': True, 'ignore_failures': False},
        {'returns': True, 'ignore_failures': True},
    ]
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
            returns = ctao.get('returns', wa.get('returns', False))
            ignore_failures = ctao.get(
                'ignore_failures',
                wa.get('ignore_failures', True)
            )
            _generate_returns_42_test(test_class, wa, ctao, returns, ignore_failures)
            _generate_raises_exc_test(test_class, wa, ctao, returns, ignore_failures)
            _generate_2in3_raises_test(test_class, wa, ctao, returns, ignore_failures)


generate_tests(TestCouplingMixin)


# ----------------------------------------------------------------------------
