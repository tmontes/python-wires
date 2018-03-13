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

from . import mixin_test_callables



class WireAssertCouplingTestMixin(mixin_test_callables.TestCallablesMixin):

    """
    Wiring and Assertion mixin for coupling tests.
    """

    def wire_returns_42_callable(self):
        """
        Wire `TestCallablesMixin.returns_42_callable` to self.w.this.
        """
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.w.this.unwire, self.returns_42_callable)


    def assert_result_wire_returns_42_callable(self, result):

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def wire_raises_exeption_callable(self):
        """
        Wire `TestCallablesMixin.raises_exception_callable` to self.w.this.
        """
        self.w.this.wire(self.raises_exception_callable)
        self.addCleanup(self.w.this.unwire, self.raises_exception_callable)


    def assert_result_wire_raises_exeption_callable(self, result):

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self.THE_EXCEPTION, None))


    def assert_failure_wire_raises_exeption_callable(self, cm):

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self.THE_EXCEPTION, None))


    def wire_three_callables_2nd_one_failing(self):
        """
        Wire three `TestCallablesMixin.*` callables to self.w.this, where the
        2nd one raises an exception, when called.
        """
        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.raises_exception_callable)
        self.w.this.wire(self.returns_none_callable)
        self.addCleanup(self.w.this.unwire, self.returns_none_callable)
        self.addCleanup(self.w.this.unwire, self.raises_exception_callable)
        self.addCleanup(self.w.this.unwire, self.returns_42_callable)


    def assert_result_wire_three_callables_2nd_one_failing(self, result):

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


    def assert_failure_wire_three_callables_2nd_one_failing(self, cm):

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self.THE_EXCEPTION, None))


    TESTS = [

    # Default Wiring instantiation arguments.

    {
        'test-name': 'test_wire_returns_42_default_call',
        'wiring-args': {},
        'wire': wire_returns_42_callable,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_default_call',
        'wiring-args': {},
        'wire': wire_raises_exeption_callable,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_default_call',
        'wiring-args': {},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_three_callables_2nd_one_failing,
    }, {
        'test-name': 'test_wire_returns_42_results_true_call',
        'wiring-args': {},
        'wire': wire_returns_42_callable,
        'args-override': {"coupling": True},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_results_true_call',
        'wiring-args': {},
        'wire': wire_raises_exeption_callable,
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'assert': assert_failure_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_results_true_call',
        'wiring-args': {},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'assert': assert_failure_wire_three_callables_2nd_one_failing,
    }, {
        'test-name': 'test_wire_returns_42_results_false_call',
        'wiring-args': {},
        'wire': wire_returns_42_callable,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_results_false_call',
        'wiring-args': {},
        'wire': wire_raises_exeption_callable,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_results_false_call',
        'wiring-args': {},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_three_callables_2nd_one_failing,
    },

    # Wiring instantiation with coupling=False

    {
        'test-name': 'test_wire_returns_42_default_call',
        'wiring-args': {"coupling": False},
        'wire': wire_returns_42_callable,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_default_call',
        'wiring-args': {"coupling": False},
        'wire': wire_raises_exeption_callable,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_default_call',
        'wiring-args': {"coupling": False},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_three_callables_2nd_one_failing,
    }, {
        'test-name': 'test_wire_returns_42_results_true_call',
        'wiring-args': {"coupling": False},
        'wire': wire_returns_42_callable,
        'args-override': {"coupling": True},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_results_true_call',
        'wiring-args': {"coupling": False},
        'wire': wire_raises_exeption_callable,
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'assert': assert_failure_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_results_true_call',
        'wiring-args': {"coupling": False},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'assert': assert_failure_wire_three_callables_2nd_one_failing,
    }, {
        'test-name': 'test_wire_returns_42_results_false_call',
        'wiring-args': {"coupling": False},
        'wire': wire_returns_42_callable,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_results_false_call',
        'wiring-args': {"coupling": False},
        'wire': wire_raises_exeption_callable,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_results_false_call',
        'wiring-args': {"coupling": False},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_three_callables_2nd_one_failing,
    },

    # Wiring instantiation with coupling=True

    {
        'test-name': 'test_wire_returns_42_default_call',
        'wiring-args': {"coupling": True},
        'wire': wire_returns_42_callable,
        'args-override': {},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_default_call',
        'wiring-args': {"coupling": True},
        'wire': wire_raises_exeption_callable,
        'args-override': {},
        'raises': RuntimeError,
        'assert': assert_failure_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_default_call',
        'wiring-args': {"coupling": True},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {},
        'raises': RuntimeError,
        'assert': assert_failure_wire_three_callables_2nd_one_failing,
    }, {
        'test-name': 'test_wire_returns_42_results_true_call',
        'wiring-args': {"coupling": True},
        'wire': wire_returns_42_callable,
        'args-override': {"coupling": True},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_results_true_call',
        'wiring-args': {"coupling": True},
        'wire': wire_raises_exeption_callable,
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'assert': assert_failure_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_results_true_call',
        'wiring-args': {"coupling": True},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'assert': assert_failure_wire_three_callables_2nd_one_failing,
    }, {
        'test-name': 'test_wire_returns_42_results_false_call',
        'wiring-args': {"coupling": True},
        'wire': wire_returns_42_callable,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_returns_42_callable,
    }, {
        'test-name': 'test_wire_raises_exception_results_false_call',
        'wiring-args': {"coupling": True},
        'wire': wire_raises_exeption_callable,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_raises_exeption_callable,
    }, {
        'test-name': 'test_wire_wire_wire_results_false_call',
        'wiring-args': {"coupling": True},
        'wire': wire_three_callables_2nd_one_failing,
        'args-override': {"coupling": False},
        'raises': None,
        'assert': assert_result_wire_three_callables_2nd_one_failing,
    }
    
    ]



class TestCouplingMixin(WireAssertCouplingTestMixin):

    """
    Drives Wires call coupling tests.
    """

    # Tests added via create_test_methods, below.



def _create_test_method(test_dict):

    wiring_args = test_dict['wiring-args']
    wire_callable = test_dict['wire']
    args_override = test_dict['args-override']
    raises = test_dict['raises']
    assert_callable = test_dict['assert']

    def test(self):
        if wiring_args:
            self.w = Wiring(**wiring_args)
        wire_callable(self)
        if raises:
            with self.assertRaises(raises) as result:
                self.w(**args_override).this()
        else:
            result = self.w(**args_override).this()
        assert_callable(self, result)

    return test



def create_test_methods(test_class, wiring_args=None):
    """
    Creates test methods on `test_class` having a `TESTS` test description list.
    Test methods with be created if:
    - The test description dict 'wiring-args' key matches `wiring_args`.
    """
    for test_dict in test_class.TESTS:
        test_wiring_args = test_dict['wiring-args']
        if wiring_args is None:
            if test_wiring_args:
                # skip test with wiring args generation
                continue
        else:
            skip = False
            for arg, value in wiring_args.items():
                if test_wiring_args.get(arg) != value:
                    # skip test with differet wiring args generation
                    skip = True
                    break
            if skip:
                continue
        test_method = _create_test_method(test_dict)
        test_method_name = test_dict['test-name']
        setattr(test_class, test_method_name, test_method)



create_test_methods(TestCouplingMixin)


# ----------------------------------------------------------------------------
