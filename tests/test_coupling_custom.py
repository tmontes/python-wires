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



class _TestWiresCouplingMixin(object):

    """
    Caller/callee custom coupling tests for Wires instances.
    """

    @staticmethod
    def _returns_42_callee():

        return 42


    @staticmethod
    def _returns_None_callee():

        return None


    _THE_EXCEPTION = ValueError('bad value detail')

    def _raises_exception_callee(self):

        raise self._THE_EXCEPTION


    def _unwire_call(self, callee):

        self.w.unwire.this.calls_to(callee)


    def wire_returns_42_callee(self):

        self.w.wire.this.calls_to(self._returns_42_callee)
        self.addCleanup(self._unwire_call, self._returns_42_callee)


    def wire_raises_exeption_callee(self):

        self.w.wire.this.calls_to(self._raises_exception_callee)
        self.addCleanup(self._unwire_call, self._raises_exception_callee)


    def wire_three_callees_2nd_one_failing(self):

        self.w.wire.this.calls_to(self._returns_42_callee)
        self.w.wire.this.calls_to(self._raises_exception_callee)
        self.w.wire.this.calls_to(self._returns_None_callee)
        self.addCleanup(self._unwire_call, self._returns_None_callee)
        self.addCleanup(self._unwire_call, self._raises_exception_callee)
        self.addCleanup(self._unwire_call, self._returns_42_callee)



class TestWiresCouplingTrue(_TestWiresCouplingMixin, unittest.TestCase):

    """
    Caller/callee explicit default coupled tests for Wires instances.
    """

    def setUp(self):

        self.w = Wiring(coupling=True)


    def test_wire_default_coupled_call(self):

        self.wire_returns_42_callee()

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_default_coupled_fail(self):

        self.wire_raises_exeption_callee()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self._THE_EXCEPTION, None))
    

    def test_wire_wire_wire_default_coupled_fail(self):

        self.wire_three_callees_2nd_one_failing()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self._THE_EXCEPTION, None))


    def test_wire_coupled_call(self):

        self.wire_returns_42_callee()

        result = self.w.coupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_coupled_fail(self):

        self.wire_raises_exeption_callee()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.coupled_call.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self._THE_EXCEPTION, None))
    

    def test_wire_wire_wire_coupled_fail(self):

        self.wire_three_callees_2nd_one_failing()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.coupled_call.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self._THE_EXCEPTION, None))


    def test_wire_decoupled_call(self):

        self.wire_returns_42_callee()

        result = self.w.decoupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_decoupled_fail(self):

        self.wire_raises_exeption_callee()

        result = self.w.decoupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self._THE_EXCEPTION, None))
    

    def test_wire_wire_wire_decoupled_fail(self):

        self.wire_three_callees_2nd_one_failing()

        result = self.w.decoupled_call.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self._THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))



class TestWiresCouplingFalse(_TestWiresCouplingMixin, unittest.TestCase):

    """
    Caller/callee explicit default decoupled tests for Wires instances.
    """

    def setUp(self):

        self.w = Wiring(coupling=False)


    def test_wire_default_decoupled_call(self):

        self.wire_returns_42_callee()

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_default_decoupled_fail(self):

        self.wire_raises_exeption_callee()

        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self._THE_EXCEPTION, None))
    

    def test_wire_wire_wire_default_decoupled_fail(self):

        self.wire_three_callees_2nd_one_failing()

        result = self.w.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self._THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


    def test_wire_coupled_call(self):

        self.wire_returns_42_callee()

        result = self.w.coupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_coupled_fail(self):

        self.wire_raises_exeption_callee()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.coupled_call.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self._THE_EXCEPTION, None))
    

    def test_wire_wire_wire_coupled_fail(self):

        self.wire_three_callees_2nd_one_failing()

        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.coupled_call.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self._THE_EXCEPTION, None))


    def test_wire_decoupled_call(self):

        self.wire_returns_42_callee()

        result = self.w.decoupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_decoupled_fail(self):

        self.wire_raises_exeption_callee()

        result = self.w.decoupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self._THE_EXCEPTION, None))
    

    def test_wire_wire_wire_decoupled_fail(self):

        self.wire_three_callees_2nd_one_failing()

        result = self.w.decoupled_call.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self._THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


# ----------------------------------------------------------------------------