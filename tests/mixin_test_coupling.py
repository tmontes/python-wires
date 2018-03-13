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


    TESTS = [{
        # Default Wiring instantiation arguments.
        'wiring-args': {},
        'tests': [{
            'test-name': 'test_wire_returns_42_default_call',
            'wirings': [return_42],
            'args-override': {},
            'raises': None,
            'result': [(None, 42)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_default_call',
            'wirings': [raise_exception],
            'args-override': {},
            'raises': None,
            'result': [(EXCEPTION, None)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_default_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None)],
            'call-counts': [1, 1, 1],
        }, {
            'test-name': 'test_wire_returns_42_coupling_true_call',
            'wirings': [return_42],
            'args-override': {"coupling": True},
            'raises': None,
            'result': [(None, 42)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_coupling_true_call',
            'wirings': [raise_exception],
            'args-override': {"coupling": True},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_coupling_true_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {"coupling": True},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call-counts': [1, 1, 0],
        }, {
            'test-name': 'test_wire_returns_42_coupling_false_call',
            'wirings': [return_42],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(None, 42)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_coupling_false_call',
            'wirings': [raise_exception],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(EXCEPTION, None)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_coupling_false_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None)],
            'call-counts': [1, 1, 1],
        }]
    }, {
        # Wiring instantiation with coupling=False
        'wiring-args': {"coupling": False},
        'tests': [{
            'test-name': 'test_wire_returns_42_default_call',
            'wirings': [return_42],
            'args-override': {},
            'raises': None,
            'result': [(None, 42)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_default_call',
            'wirings': [raise_exception],
            'args-override': {},
            'raises': None,
            'result': [(EXCEPTION, None)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_default_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None)],
            'call-counts': [1, 1, 1],
        }, {
            'test-name': 'test_wire_returns_42_coupling_true_call',
            'wirings': [return_42],
            'args-override': {"coupling": True},
            'raises': None,
            'result': [(None, 42)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_coupling_true_call',
            'wirings': [raise_exception],
            'args-override': {"coupling": True},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_coupling_true_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {"coupling": True},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call-counts': [1, 1, 0],
        }, {
            'test-name': 'test_wire_returns_42_coupling_false_call',
            'wirings': [return_42],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(None, 42)],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_coupling_false_call',
            'wirings': [raise_exception],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(EXCEPTION, None),],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_coupling_false_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None),],
            'call-counts': [1, 1, 1],
        },

        ]
    }, {
        # Wiring instantiation with coupling=True
        'wiring-args': {"coupling": True},
        'tests': [{
            'test-name': 'test_wire_returns_42_default_call',
            'wirings': [return_42],
            'args-override': {},
            'raises': None,
            'result': [(None, 42),],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_default_call',
            'wirings': [raise_exception],
            'args-override': {},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_default_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call-counts': [1, 1, 0],
        }, {
            'test-name': 'test_wire_returns_42_coupling_true_call',
            'wirings': [return_42],
            'args-override': {"coupling": True},
            'raises': None,
            'result': [(None, 42),],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_coupling_true_call',
            'wirings': [raise_exception],
            'args-override': {"coupling": True},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_coupling_true_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {"coupling": True},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call-counts': [1, 1, 0],
        }, {
            'test-name': 'test_wire_returns_42_coupling_false_call',
            'wirings': [return_42],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(None, 42),],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_raises_exception_coupling_false_call',
            'wirings': [raise_exception],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(EXCEPTION, None),],
            'call-counts': [1],
        }, {
            'test-name': 'test_wire_wire_wire_coupling_false_call',
            'wirings': [return_42, raise_exception, return_none],
            'args-override': {"coupling": False},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None),],
            'call-counts': [1, 1, 1],
        }],
    }]



class TestCouplingMixin(WireAssertCouplingTestMixin):

    """
    Drives Wires call coupling tests.
    """

    # Tests added via create_test_methods, below.



def _create_test_method(wiring_args, test_entry):

    wirings = test_entry['wirings']
    args_override = test_entry['args-override']
    raises = test_entry['raises']
    expected_result = test_entry['result']
    expected_call_counts = test_entry['call-counts']

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
    Entries in such list have two keys:
    - `wiring-args`: Wiring initialization arguments for the associated `tests`.
    - `tests`: List of test specifications.
    Tests will only be created for matching wiring arguments.
    """
    for test_set in test_class.TESTS:
        test_set_wiring_args = test_set['wiring-args']
        if wiring_args is None:
            if test_set_wiring_args:
                # no wiring_args: skip test sets with wiring args.
                continue
        else:
            skip = False
            for arg, value in wiring_args.items():
                if test_set_wiring_args.get(arg) != value:
                    # skip test sets with differet wiring args
                    skip = True
                    break
            if skip:
                continue
        # create the test methods
        for test_entry in test_set['tests']:
            test_method = _create_test_method(test_set_wiring_args, test_entry)
            test_method_name = test_entry['test-name']
            setattr(test_class, test_method_name, test_method)



create_test_methods(TestCouplingMixin)


# ----------------------------------------------------------------------------
