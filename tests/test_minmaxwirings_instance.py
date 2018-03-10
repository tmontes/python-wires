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

        w.this.wire(self.returns_42_callable)
        w.this.unwire(self.returns_42_callable)


    def test_min_1_wire_unwire_raises_runtime_error(self):
        """
        Wiring then unwiring with min_wirings=1 raises a RuntimeError.
        """
        w = Wiring(min_wirings=1)

        w.this.wire(self.returns_42_callable)
        with self.assertRaises(RuntimeError) as cm:
            w.this.unwire(self.returns_42_callable)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings limit reached')


    def test_max_1_wire_wire_raises_runtime_error(self):
        """
        Wiring two callables with max_wirings=1 raises a RuntimeError.
        """
        w = Wiring(max_wirings=1)

        w.this.wire(self.returns_42_callable)
        with self.assertRaises(RuntimeError) as cm:
            w.this.wire(self.returns_42_callable)

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

        w.this.wire(self.returns_42_callable)
        result = w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))



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
        self.w.this.wire(self.returns_42_callable)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        self.addCleanup(self.reset_min_max_wirings)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this.unwire(self.returns_42_callable)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'min_wirings limit reached')


    def test_max_1_wire_wire_raises_runtime_error(self):
        """
        Wiring two callables with max_wirings=1 raises a RuntimeError.
        """
        self.w.this.max_wirings = 1
        self.w.this.wire(self.returns_42_callable)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        self.addCleanup(self.reset_min_max_wirings)

        with self.assertRaises(RuntimeError) as cm:
            self.w.this.wire(self.returns_42_callable)

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
        self.w.this.wire(self.returns_42_callable)

        # clean up in the reverse order, otherwise unwiring fails
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        self.addCleanup(self.reset_min_max_wirings)

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_min_2_raises_value_error(self):
        """
        Setting min_wirings < wired callables raises ValueError.
        """
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)

        with self.assertRaises(ValueError) as cm:
            self.w.this.min_wirings = 2

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too few wirings')


    def test_wire_wire_max_1_raises_value_error(self):
        """
        Setting min_wirings < wired callables raises ValueError.
        """
        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)

        with self.assertRaises(ValueError) as cm:
            self.w.this.max_wirings = 1

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'too many wirings')


# ----------------------------------------------------------------------------
