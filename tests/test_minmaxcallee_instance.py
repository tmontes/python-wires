# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance min/max callee tests.
"""


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_callees



class TestInstanceMinMaxCallee(mixin_test_callees.TestCalleesMixin,
                               unittest.TestCase):

    """
    min/max callee tests for Wires instances.
    """

    def test_non_positive_min_raises_value_error(self):
        """
        Passing N <= 0 as `min_callees` raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            _ = Wiring(min_callees=-42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_callees must be positive or None')


    def test_non_positive_max_raises_value_error(self):
        """
        Passing N <= 0 as `max_callees` raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            _ = Wiring(max_callees=-42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_callees must be positive or None')


    def test_min_callee_greater_than_max_callee_raises_value_error(self):
        """
        Passing `min_callees` > `max_callees` raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            _ = Wiring(min_callees=42, max_callees=24)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_callees must be >= min_callees')


    def test_min_none_max_none_wire_unwire(self):
        """
        Wiring a single callable works.
        """
        w = Wiring(min_callees=None, max_callees=None)

        w.this.wire(self.returns_42_callee)
        w.this.unwire(self.returns_42_callee)


    def test_min_1_wire_unwire_raises_runtime_error(self):
        """
        Wiring then unwiring with min_callee=1 raises a RuntimeError.
        """
        w = Wiring(min_callees=1)

        w.this.wire(self.returns_42_callee)
        with self.assertRaises(RuntimeError) as cm:
            w.this.unwire(self.returns_42_callee)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_callees limit reached')


    def test_max_1_wire_wire_raises_runtime_error(self):
        """
        Wiring two callables with max_callee=1 raises a RuntimeError.
        """
        w = Wiring(max_callees=1)

        w.this.wire(self.returns_42_callee)
        with self.assertRaises(RuntimeError) as cm:
            w.this.wire(self.returns_42_callee)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_callees limit reached')


    def test_min_1_call_raises_runtime_error(self):
        """
        Calling an unwired callable with min_callees set raises RuntimeError.
        """
        w = Wiring(min_callees=1)

        with self.assertRaises(RuntimeError) as cm:
            w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'less than min_callees wired')


    def test_min_1_wire_call(self):
        """
        Calling a wired callable with min_callees works.
        """
        w = Wiring(min_callees=1)

        w.this.wire(self.returns_42_callee)
        result = w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))



class TestCallableMinMaxCallee(mixin_test_callees.TestCalleesMixin,
                               unittest.TestCase):

    """
    Per callable min/max callee tests.
    """

    def setUp(self):

        self.w = Wiring()


    def test_min_callees_defaults_to_none(self):
        """
        Callable `min_callees` defaults to None.
        """
        result = self.w.this.min_callees
        self.assertIsNone(result)


    def test_max_callees_defaults_to_none(self):
        """
        Callable `max_callees` defaults to None.
        """
        result = self.w.this.max_callees
        self.assertIsNone(result)


    def test_non_positive_min_raises_value_error(self):
        """
        Setting callable `min_callees` to N <= 0 raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            self.w.this.min_callees = -42

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_callees must be positive or None')


    def test_non_positive_max_raises_value_error(self):
        """
        Setting callable `max_callees` to N <= 0 raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            self.w.this.max_callees = -42

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_callees must be positive or None')


    def test_min_callee_greater_than_max_callee_raises_value_error(self):
        """
        Setting callable `min_callees` > `max_callees` raises a ValueError.
        """
        self.w.this.max_callees = 24
        with self.assertRaises(ValueError) as cm:
            self.w.this.min_callees = 42

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_callees must be <= max_callees')


    def test_max_callee_less_than_mmin_callee_raises_value_error(self):
        """
        Setting callable `max_callees` < `min_callees` raises a ValueError.
        """
        self.w.this.min_callees = 42
        with self.assertRaises(ValueError) as cm:
            self.w.this.max_callees = 24

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_callees must be >= min_callees')


    def reset_min_max_callee(self):
        """
        Used in test cleanups.
        """
        self.w.this.min_callees = None
        self.w.this.max_callees = None


    def test_min_1_wire_unwire_raises_runtime_error(self):
        """
        Wiring then unwiring with min_callee=1 raises a RuntimeError.
        """
        self.w.this.min_callees = 1
        self.w.this.wire(self.returns_42_callee)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.unwire_call, self.returns_42_callee)
        self.addCleanup(self.reset_min_max_callee)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this.unwire(self.returns_42_callee)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_callees limit reached')


    def test_max_1_wire_wire_raises_runtime_error(self):
        """
        Wiring two callables with max_callee=1 raises a RuntimeError.
        """
        self.w.this.max_callees = 1
        self.w.this.wire(self.returns_42_callee)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.unwire_call, self.returns_42_callee)
        self.addCleanup(self.reset_min_max_callee)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this.wire(self.returns_42_callee)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_callees limit reached')


    def test_min_1_call_raises_runtime_error(self):
        """
        Calling an unwired callable with min_callees set raises RuntimeError.
        """
        self.w.this.min_callees = 1
        self.addCleanup(self.reset_min_max_callee)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'less than min_callees wired')


    def test_min_1_wire_call(self):
        """
        Calling a wired callable with min_callees works.
        """
        self.w.this.min_callees = 1
        self.w.this.wire(self.returns_42_callee)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.unwire_call, self.returns_42_callee)
        self.addCleanup(self.reset_min_max_callee)

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_min_2_raises_value_error(self):
        """
        Setting min_callees < wired callees raises ValueError.
        """
        self.w.this.wire(self.returns_42_callee)
        self.addCleanup(self.unwire_call, self.returns_42_callee)

        with self.assertRaises(ValueError) as cm:
            self.w.this.min_callees = 2

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too few wired callees')


    def test_wire_wire_max_1_raises_value_error(self):
        """
        Setting min_callees < wired callees raises ValueError.
        """
        self.w.this.wire(self.returns_42_callee)
        self.w.this.wire(self.returns_42_callee)
        self.addCleanup(self.unwire_call, self.returns_42_callee)
        self.addCleanup(self.unwire_call, self.returns_42_callee)

        with self.assertRaises(ValueError) as cm:
            self.w.this.max_callees = 1

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too many wired callees')


# ----------------------------------------------------------------------------
