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



class TestMinMaxCallee(mixin_test_callees.TestCalleesMixin, unittest.TestCase):

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

        w.wire.this.calls_to(self.returns_42_callee)
        w.unwire.this.calls_to(self.returns_42_callee)


# ----------------------------------------------------------------------------
