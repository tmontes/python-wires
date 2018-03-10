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

from . import mixin_test_callables



class _TestWiresCouplingMixin(mixin_test_callables.TestCallablesMixin):

    """
    Caller/callee custom coupling tests for Wires instances.
    """

    def wire_returns_42_callable(self):

        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)


    def wire_raises_exeption_callable(self):

        self.w.this.wire(self.raises_exception_callable)
        self.addCleanup(self.unwire_call, self.raises_exception_callable)


    def wire_three_callables_2nd_one_failing(self):

        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.raises_exception_callable)
        self.w.this.wire(self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.raises_exception_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)



class TestWiresCouplingTrue(_TestWiresCouplingMixin, unittest.TestCase):

    """
    Caller/callee explicit default coupled tests for Wires instances.
    """

    def setUp(self):

        self.w = Wiring(coupling=True)


    def test_wire_default_coupled_call(self):

        self.wire_returns_42_callable()

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_default_coupled_fail(self):

        self.wire_raises_exeption_callable()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self.THE_EXCEPTION, None))
    

    def test_wire_wire_wire_default_coupled_fail(self):

        self.wire_three_callables_2nd_one_failing()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self.THE_EXCEPTION, None))


    def test_wire_coupled_call(self):

        self.wire_returns_42_callable()

        result = self.w.couple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_coupled_fail(self):

        self.wire_raises_exeption_callable()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self.THE_EXCEPTION, None))
    

    def test_wire_wire_wire_coupled_fail(self):

        self.wire_three_callables_2nd_one_failing()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self.THE_EXCEPTION, None))


    def test_wire_decoupled_call(self):

        self.wire_returns_42_callable()

        result = self.w.decouple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_decoupled_fail(self):

        self.wire_raises_exeption_callable()

        result = self.w.decouple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self.THE_EXCEPTION, None))
    

    def test_wire_wire_wire_decoupled_fail(self):

        self.wire_three_callables_2nd_one_failing()

        result = self.w.decouple.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))



class TestWiresCouplingFalse(_TestWiresCouplingMixin, unittest.TestCase):

    """
    Caller/callee explicit default decoupled tests for Wires instances.
    """

    def setUp(self):

        self.w = Wiring(coupling=False)


    def test_wire_default_decoupled_call(self):

        self.wire_returns_42_callable()

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_default_decoupled_fail(self):

        self.wire_raises_exeption_callable()

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self.THE_EXCEPTION, None))
    

    def test_wire_wire_wire_default_decoupled_fail(self):

        self.wire_three_callables_2nd_one_failing()

        result = self.w.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


    def test_wire_coupled_call(self):

        self.wire_returns_42_callable()

        result = self.w.couple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_coupled_fail(self):

        self.wire_raises_exeption_callable()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self.THE_EXCEPTION, None))
    

    def test_wire_wire_wire_coupled_fail(self):

        self.wire_three_callables_2nd_one_failing()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.couple.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self.THE_EXCEPTION, None))


    def test_wire_decoupled_call(self):

        self.wire_returns_42_callable()

        result = self.w.decouple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_decoupled_fail(self):

        self.wire_raises_exeption_callable()

        result = self.w.decouple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self.THE_EXCEPTION, None))
    

    def test_wire_wire_wire_decoupled_fail(self):

        self.wire_three_callables_2nd_one_failing()

        result = self.w.decouple.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


# ----------------------------------------------------------------------------
