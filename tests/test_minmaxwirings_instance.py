# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance min/max wirings tests.
"""


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_callables



class TestInstanceMinMaxWirings(mixin_test_callables.TestCallablesMixin,
                                unittest.TestCase):

    """
    min/max wirings tests for Wires instances.
    """

    def test_non_positive_min_raises_value_error(self):
        """
        Passing N <= 0 as `min_wirings` raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            _ = Wiring(min_wirings=-42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings must be positive or None')


    def test_non_positive_max_raises_value_error(self):
        """
        Passing N <= 0 as `max_wirings` raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            _ = Wiring(max_wirings=-42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_wirings must be positive or None')


    def test_min_wirings_greater_than_max_wirings_raises_value_error(self):
        """
        Passing `min_wirings` > `max_wirings` raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            _ = Wiring(min_wirings=42, max_wirings=24)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_wirings must be >= min_wirings')


    def test_min_none_max_none_wire_unwire(self):
        """
        Wiring a single callable works.
        """
        w = Wiring(min_wirings=None, max_wirings=None)

        w.this.wire(self.returns_42)
        w.this.unwire(self.returns_42)


    def test_min_1_wire_unwire_raises_runtime_error(self):
        """
        Wiring then unwiring with min_wirings=1 raises a RuntimeError.
        """
        w = Wiring(min_wirings=1)

        w.this.wire(self.returns_42)
        with self.assertRaises(RuntimeError) as cm:
            w.this.unwire(self.returns_42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings limit reached')


    def test_max_1_wire_wire_raises_runtime_error(self):
        """
        Wiring two callables with max_wirings=1 raises a RuntimeError.
        """
        w = Wiring(max_wirings=1)

        w.this.wire(self.returns_42)
        with self.assertRaises(RuntimeError) as cm:
            w.this.wire(self.returns_42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_wirings limit reached')


    def test_min_1_call_raises_runtime_error(self):
        """
        Calling an unwired callable with min_wirings set raises RuntimeError.
        """
        w = Wiring(min_wirings=1)

        with self.assertRaises(RuntimeError) as cm:
            w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'less than min_wirings wired')


    def test_min_1_wire_call(self):
        """
        Calling a wired callable with min_wirings works.
        """
        w = Wiring(min_wirings=1)

        w.this.wire(self.returns_42)
        result = w.this()

        self.assertIsNone(result)



class TestCallableMinMaxWirings(mixin_test_callables.TestCallablesMixin,
                                unittest.TestCase):

    """
    Per callable min/max wirings tests.
    """

    def setUp(self):

        self.w = Wiring()


    def test_min_wirings_defaults_to_none(self):
        """
        Callable `min_wirings` defaults to None.
        """
        result = self.w.this.min_wirings
        self.assertIsNone(result)


    def test_max_wirings_defaults_to_none(self):
        """
        Callable `max_wirings` defaults to None.
        """
        result = self.w.this.max_wirings
        self.assertIsNone(result)


    def test_non_positive_min_raises_value_error(self):
        """
        Setting callable `min_wirings` to N <= 0 raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            self.w.this.min_wirings = -42

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings must be positive or None')


    def test_non_positive_max_raises_value_error(self):
        """
        Setting callable `max_wirings` to N <= 0 raises a ValueError.
        """
        with self.assertRaises(ValueError) as cm:
            self.w.this.max_wirings = -42

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_wirings must be positive or None')


    def test_min_wirings_greater_than_max_wirings_raises_value_error(self):
        """
        Setting callable `min_wirings` > `max_wirings` raises a ValueError.
        """
        self.w.this.max_wirings = 24
        with self.assertRaises(ValueError) as cm:
            self.w.this.min_wirings = 42

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings must be <= max_wirings')


    def test_max_wirings_less_than_mmin_wirings_raises_value_error(self):
        """
        Setting callable `max_wirings` < `min_wirings` raises a ValueError.
        """
        self.w.this.min_wirings = 42
        with self.assertRaises(ValueError) as cm:
            self.w.this.max_wirings = 24

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_wirings must be >= min_wirings')


    def reset_min_max_wirings(self):
        """
        Used in test cleanups.
        """
        self.w.this.min_wirings = None
        self.w.this.max_wirings = None


    def test_min_1_wire_unwire_raises_runtime_error(self):
        """
        Wiring then unwiring with min_wirings=1 raises a RuntimeError.
        """
        self.w.this.min_wirings = 1
        self.w.this.wire(self.returns_42)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.w.this.unwire, self.returns_42)
        self.addCleanup(self.reset_min_max_wirings)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this.unwire(self.returns_42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings limit reached')


    def test_max_1_wire_wire_raises_runtime_error(self):
        """
        Wiring two callables with max_wirings=1 raises a RuntimeError.
        """
        self.w.this.max_wirings = 1
        self.w.this.wire(self.returns_42)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.w.this.unwire, self.returns_42)
        self.addCleanup(self.reset_min_max_wirings)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this.wire(self.returns_42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'max_wirings limit reached')


    def test_min_1_call_raises_runtime_error(self):
        """
        Calling an unwired callable with min_wirings set raises RuntimeError.
        """
        self.w.this.min_wirings = 1
        self.addCleanup(self.reset_min_max_wirings)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'less than min_wirings wired')


    def test_min_1_wire_call(self):
        """
        Calling a wired callable with min_wirings works.
        """
        self.w.this.min_wirings = 1
        self.w.this.wire(self.returns_42)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.w.this.unwire, self.returns_42)
        self.addCleanup(self.reset_min_max_wirings)

        result = self.w.this()

        self.assertIsNone(result)


    def test_wire_min_2_raises_value_error(self):
        """
        Setting min_wirings < wired callables raises ValueError.
        """
        self.w.this.wire(self.returns_42)
        self.addCleanup(self.w.this.unwire, self.returns_42)

        with self.assertRaises(ValueError) as cm:
            self.w.this.min_wirings = 2

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too few wirings')


    def test_wire_wire_max_1_raises_value_error(self):
        """
        Setting min_wirings < wired callables raises ValueError.
        """
        self.w.this.wire(self.returns_42)
        self.w.this.wire(self.returns_42)
        self.addCleanup(self.w.this.unwire, self.returns_42)
        self.addCleanup(self.w.this.unwire, self.returns_42)

        with self.assertRaises(ValueError) as cm:
            self.w.this.max_wirings = 1

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too many wirings')



class TestCombinedMinMaxWirings(mixin_test_callables.TestCallablesMixin,
                                unittest.TestCase):

    """
    Combined wiring and callable min/max wirings tests.
    """

    def test_callable_cant_revert_to_instance_min_wirings(self):
        """
        Deleting callable `min_wirings` fails if the resulting value (the
        Wiring instance's) would leave the callable in an invalid state.
        """
        w = Wiring(min_wirings=2)

        w.this.min_wirings = None

        w.this.wire(self.returns_42)
        self.addCleanup(w.this.unwire, self.returns_42)

        # Resetting per-callable min_wirings should fail: it would fallback
        # to the instance's min_wirings=2, but there are not enough wirings.
        with self.assertRaises(ValueError) as cm:
            del w.this.min_wirings

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too few wirings')

        # Per-callable min_wirings should be unchanged.
        self.assertIsNone(w.this.min_wirings)


    def test_callable_cant_revert_to_instance_max_wirings(self):
        """
        Deleting callable `max_wirings` fails if the resulting value (the
        Wiring instance's) would leave the callable in an invalid state.
        """
        w = Wiring(max_wirings=1)

        w.this.max_wirings = 2

        w.this.wire(self.returns_42)
        w.this.wire(self.returns_none)
        self.addCleanup(w.this.unwire, self.returns_42)
        self.addCleanup(w.this.unwire, self.returns_none)

        # Resetting per-callable max_wirings should fail: it would fallback
        # to the instance's max_wirings=1, but there are too many wirings.
        with self.assertRaises(ValueError) as cm:
            del w.this.max_wirings

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too many wirings')

        # Per-callable max_wirings should be unchanged.
        self.assertEqual(w.this.max_wirings, 2)


# ----------------------------------------------------------------------------
