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

from . helpers import CallTracker as CT



class WireAssertCouplingTestMixin(object):

    """
    Wiring and Assertion mixin for coupling tests.
    """

    EXCEPTION = ValueError('test exception message')

    TESTS = [

    # Default Wiring instantiation arguments.

    {
        'test-name': 'test_wire_returns_42_default_call',
        'wiring-args': {},
        'wirings': [CT(returns=42)],
        'args-override': {},
        'raises': None,
        'result': [(None, 42)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_default_call',
        'wiring-args': {},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {},
        'raises': None,
        'result': [(EXCEPTION, None)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_default_call',
        'wiring-args': {},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {},
        'raises': None,
        'result': [(None, 42), (EXCEPTION, None), (None, None)],
        'call-counts': [1, 1, 1],
    }, {
        'test-name': 'test_wire_returns_42_results_true_call',
        'wiring-args': {},
        'wirings': [CT(returns=42)],
        'args-override': {"coupling": True},
        'raises': None,
        'result': [(None, 42)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_results_true_call',
        'wiring-args': {},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'result': ((EXCEPTION, None),),
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_results_true_call',
        'wiring-args': {},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'result': ((None, 42), (EXCEPTION, None),),
        'call-counts': [1, 1, 0],
    }, {
        'test-name': 'test_wire_returns_42_results_false_call',
        'wiring-args': {},
        'wirings': [CT(returns=42)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(None, 42)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_results_false_call',
        'wiring-args': {},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(EXCEPTION, None)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_results_false_call',
        'wiring-args': {},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(None, 42), (EXCEPTION, None), (None, None)],
        'call-counts': [1, 1, 1],
    },

    # Wiring instantiation with coupling=False

    {
        'test-name': 'test_wire_returns_42_default_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(returns=42)],
        'args-override': {},
        'raises': None,
        'result': [(None, 42)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_default_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {},
        'raises': None,
        'result': [(EXCEPTION, None)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_default_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {},
        'raises': None,
        'result': [(None, 42), (EXCEPTION, None), (None, None)],
        'call-counts': [1, 1, 1],
    }, {
        'test-name': 'test_wire_returns_42_results_true_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(returns=42)],
        'args-override': {"coupling": True},
        'raises': None,
        'result': [(None, 42)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_results_true_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'result': ((EXCEPTION, None),),
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_results_true_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'result': ((None, 42), (EXCEPTION, None),),
        'call-counts': [1, 1, 0],
    }, {
        'test-name': 'test_wire_returns_42_results_false_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(returns=42)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(None, 42)],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_results_false_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(EXCEPTION, None),],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_results_false_call',
        'wiring-args': {"coupling": False},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(None, 42), (EXCEPTION, None), (None, None),],
        'call-counts': [1, 1, 1],
    },

    # Wiring instantiation with coupling=True

    {
        'test-name': 'test_wire_returns_42_default_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(returns=42)],
        'args-override': {},
        'raises': None,
        'result': [(None, 42),],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_default_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {},
        'raises': RuntimeError,
        'result': ((EXCEPTION, None),),
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_default_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {},
        'raises': RuntimeError,
        'result': ((None, 42), (EXCEPTION, None),),
        'call-counts': [1, 1, 0],
    }, {
        'test-name': 'test_wire_returns_42_results_true_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(returns=42)],
        'args-override': {"coupling": True},
        'raises': None,
        'result': [(None, 42),],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_results_true_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'result': ((EXCEPTION, None),),
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_results_true_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {"coupling": True},
        'raises': RuntimeError,
        'result': ((None, 42), (EXCEPTION, None),),
        'call-counts': [1, 1, 0],
    }, {
        'test-name': 'test_wire_returns_42_results_false_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(returns=42)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(None, 42),],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_raises_exception_results_false_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(raises=EXCEPTION)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(EXCEPTION, None),],
        'call-counts': [1],
    }, {
        'test-name': 'test_wire_wire_wire_results_false_call',
        'wiring-args': {"coupling": True},
        'wirings': [CT(returns=42), CT(raises=EXCEPTION), CT(returns=None)],
        'args-override': {"coupling": False},
        'raises': None,
        'result': [(None, 42), (EXCEPTION, None), (None, None),],
        'call-counts': [1, 1, 1],
    }
    
    ]



class TestCouplingMixin(WireAssertCouplingTestMixin):

    """
    Drives Wires call coupling tests.
    """

    # Tests added via create_test_methods, below.



def _create_test_method(test_dict):

    wiring_args = test_dict['wiring-args']
    wirings = test_dict['wirings']
    args_override = test_dict['args-override']
    raises = test_dict['raises']
    expected_result = test_dict['result']
    expected_call_counts = test_dict['call-counts']

    def test(self):
        if wiring_args:
            self.w = Wiring(**wiring_args)
        for wiring in wirings:
            wiring.reset()
            self.w.this.wire(wiring)
            self.addCleanup(self.w.this.unwire, wiring)
        if raises:
            with self.assertRaises(raises) as cm:
                self.w(**args_override).this()
            result = cm.exception.args
        else:
            result = self.w(**args_override).this()
        call_counts = [w.call_count for w in wirings]
        self.assertEqual(expected_call_counts, call_counts, 'call count mismatch')
        self.assertEqual(expected_result, result, 'result mismatch')

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
