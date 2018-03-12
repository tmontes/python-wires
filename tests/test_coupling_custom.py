# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance caller/callee custom coupling tests.
"""


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_coupling



class TestWiresCouplingTrue(mixin_test_coupling.WireAssertCouplingTestMixin,
                            unittest.TestCase):

    """
    Caller/callee explicit default coupled tests for Wires instances.
    """

    def setUp(self):

        self.w = Wiring(coupling=True)


    def test_wire_default_coupled_call(self):

        self.wire_returns_42_callable()
        result = self.w.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_default_coupled_fail(self):

        self.wire_raises_exeption_callable()
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()
        self.assert_failure_wire_raises_exeption_callable(cm)


    def test_wire_wire_wire_default_coupled_fail(self):

        self.wire_three_callables_2nd_one_failing()
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()
        self.assert_failure_wire_three_callables_2nd_one_failing(cm)


    def test_wire_coupled_call(self):

        self.wire_returns_42_callable()
        result = self.w.couple.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_coupled_fail(self):

        self.wire_raises_exeption_callable()
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()
        self.assert_failure_wire_raises_exeption_callable(cm)


    def test_wire_wire_wire_coupled_fail(self):

        self.wire_three_callables_2nd_one_failing()
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()
        self.assert_failure_wire_three_callables_2nd_one_failing(cm)


    def test_wire_decoupled_call(self):

        self.wire_returns_42_callable()
        result = self.w.decouple.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_decoupled_fail(self):

        self.wire_raises_exeption_callable()
        result = self.w.decouple.this()
        self.assert_result_wire_raises_exeption_callable(result)


    def test_wire_wire_wire_decoupled_fail(self):

        self.wire_three_callables_2nd_one_failing()
        result = self.w.decouple.this()
        self.assert_result_wire_three_callables_2nd_one_failing(result)



class TestWiresCouplingFalse(mixin_test_coupling.WireAssertCouplingTestMixin,
                             unittest.TestCase):

    """
    Caller/callee explicit default decoupled tests for Wires instances.
    """

    def setUp(self):

        self.w = Wiring(coupling=False)


    def test_wire_default_decoupled_call(self):

        self.wire_returns_42_callable()
        result = self.w.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_default_decoupled_fail(self):

        self.wire_raises_exeption_callable()
        result = self.w.this()
        self.assert_result_wire_raises_exeption_callable(result)


    def test_wire_wire_wire_default_decoupled_fail(self):

        self.wire_three_callables_2nd_one_failing()
        result = self.w.this()
        self.assert_result_wire_three_callables_2nd_one_failing(result)


    def test_wire_coupled_call(self):

        self.wire_returns_42_callable()
        result = self.w.couple.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_coupled_fail(self):

        self.wire_raises_exeption_callable()
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()
        self.assert_failure_wire_raises_exeption_callable(cm)


    def test_wire_wire_wire_coupled_fail(self):

        self.wire_three_callables_2nd_one_failing()
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()
        self.assert_failure_wire_three_callables_2nd_one_failing(cm)


    def test_wire_decoupled_call(self):

        self.wire_returns_42_callable()
        result = self.w.decouple.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_decoupled_fail(self):

        self.wire_raises_exeption_callable()
        result = self.w.decouple.this()
        self.assert_result_wire_raises_exeption_callable(result)


    def test_wire_wire_wire_decoupled_fail(self):

        self.wire_three_callables_2nd_one_failing()
        result = self.w.decouple.this()
        self.assert_result_wire_three_callables_2nd_one_failing(result)


# ----------------------------------------------------------------------------
