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
        'wiring_args': {},
        'tests': [{
            'name': 'test_wire_returns_42_default_call',
            'wire': [return_42],
            'ctao': {},
            'raises': None,
            'result': [(None, 42)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_default_call',
            'wire': [raise_exception],
            'ctao': {},
            'raises': None,
            'result': [(EXCEPTION, None)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_default_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None)],
            'call_counts': [1, 1, 1],
        }, {
            'name': 'test_wire_returns_42_coupling_true_call',
            'wire': [return_42],
            'ctao': {"coupling": True},
            'raises': None,
            'result': [(None, 42)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_coupling_true_call',
            'wire': [raise_exception],
            'ctao': {"coupling": True},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_coupling_true_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {"coupling": True},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call_counts': [1, 1, 0],
        }, {
            'name': 'test_wire_returns_42_coupling_false_call',
            'wire': [return_42],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(None, 42)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_coupling_false_call',
            'wire': [raise_exception],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(EXCEPTION, None)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_coupling_false_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None)],
            'call_counts': [1, 1, 1],
        }]
    }, {
        # Wiring instantiation with coupling=False
        'wiring_args': {"coupling": False},
        'tests': [{
            'name': 'test_wire_returns_42_default_call',
            'wire': [return_42],
            'ctao': {},
            'raises': None,
            'result': [(None, 42)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_default_call',
            'wire': [raise_exception],
            'ctao': {},
            'raises': None,
            'result': [(EXCEPTION, None)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_default_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None)],
            'call_counts': [1, 1, 1],
        }, {
            'name': 'test_wire_returns_42_coupling_true_call',
            'wire': [return_42],
            'ctao': {"coupling": True},
            'raises': None,
            'result': [(None, 42)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_coupling_true_call',
            'wire': [raise_exception],
            'ctao': {"coupling": True},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_coupling_true_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {"coupling": True},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call_counts': [1, 1, 0],
        }, {
            'name': 'test_wire_returns_42_coupling_false_call',
            'wire': [return_42],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(None, 42)],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_coupling_false_call',
            'wire': [raise_exception],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(EXCEPTION, None),],
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_coupling_false_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None),],
            'call_counts': [1, 1, 1],
        },

        ]
    }, {
        # Wiring instantiation with coupling=True
        'wiring_args': {"coupling": True},
        'tests': [{
            'name': 'test_wire_returns_42_default_call',
            'wire': [return_42],
            'ctao': {},
            'raises': None,
            'result': [(None, 42),],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_default_call',
            'wire': [raise_exception],
            'ctao': {},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_default_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call_counts': [1, 1, 0],
        }, {
            'name': 'test_wire_returns_42_coupling_true_call',
            'wire': [return_42],
            'ctao': {"coupling": True},
            'raises': None,
            'result': [(None, 42),],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_coupling_true_call',
            'wire': [raise_exception],
            'ctao': {"coupling": True},
            'raises': RuntimeError,
            'result': ((EXCEPTION, None),),
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_coupling_true_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {"coupling": True},
            'raises': RuntimeError,
            'result': ((None, 42), (EXCEPTION, None),),
            'call_counts': [1, 1, 0],
        }, {
            'name': 'test_wire_returns_42_coupling_false_call',
            'wire': [return_42],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(None, 42),],
            'call_counts': [1],
        }, {
            'name': 'test_wire_raises_exception_coupling_false_call',
            'wire': [raise_exception],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(EXCEPTION, None),],
            'call_counts': [1],
        }, {
            'name': 'test_wire_wire_wire_coupling_false_call',
            'wire': [return_42, raise_exception, return_none],
            'ctao': {"coupling": False},
            'raises': None,
            'result': [(None, 42), (EXCEPTION, None), (None, None),],
            'call_counts': [1, 1, 1],
        }],
    }]



class TestCouplingMixin(WireAssertCouplingTestMixin):

    """
    Drives Wires call coupling tests.
    """

    # Tests added via create_test_methods, below.



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



def create_test_methods(test_class, wiring_args=None):
    """
    Creates test methods on `test_class` having a `TESTS` test description list.
    Entries in such list have two keys:
    - `wiring_args`: Wiring initialization arguments for the associated `tests`.
    - `tests`: List of test specifications.
    Tests will only be created for matching wiring arguments.
    """
    for test_set in test_class.TESTS:
        test_set_wiring_args = test_set['wiring_args']
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
            test_method_name = test_entry.pop('name')
            test_method = _create_test_method(test_set_wiring_args, **test_entry)
            setattr(test_class, test_method_name, test_method)



create_test_methods(TestCouplingMixin)


# ----------------------------------------------------------------------------
