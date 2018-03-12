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

from . import mixin_test_callables



class WireAssertCouplingTestMixin(mixin_test_callables.TestCallablesMixin):

    """
    Caller/callee custom coupling tests for Wires instances.
    """

    def wire_returns_42_callable(self):

        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.w.this.unwire, self.returns_42_callable)


    def assert_result_wire_returns_42_callable(self, result):

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def wire_raises_exeption_callable(self):

        self.w.this.wire(self.raises_exception_callable)
        self.addCleanup(self.w.this.unwire, self.raises_exception_callable)


    def assert_result_wire_raises_exeption_callable(self, result):

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (self.THE_EXCEPTION, None))


    def assert_failure_wire_raises_exeption_callable(self, cm):

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], (self.THE_EXCEPTION, None))


    def wire_three_callables_2nd_one_failing(self):

        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.raises_exception_callable)
        self.w.this.wire(self.returns_none_callable)
        self.addCleanup(self.w.this.unwire, self.returns_none_callable)
        self.addCleanup(self.w.this.unwire, self.raises_exception_callable)
        self.addCleanup(self.w.this.unwire, self.returns_42_callable)


    def assert_result_wire_three_callables_2nd_one_failing(self, result):

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


    def assert_failure_wire_three_callables_2nd_one_failing(self, cm):

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self.THE_EXCEPTION, None))



class TestCallerCalleeCouplingMixin(WireAssertCouplingTestMixin):

    """
    Drives Wires caller/callee coupling tests requiring mixed class to:
    - Have a Wiring instance at self.w.
    - Allow wiring via self.wire.
    - Allow unwiring via self.unwire.
    """

    def test_wire_default_decoupled_call(self):
        """
        Default uncoupled test: return a list of (<exception>, <result>), per-
        callee tuple.
        """
        self.wire_returns_42_callable()
        result = self.w.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_wire_wire_default_decoupled_call(self):
        """
        Default uncoupled test: return a list of (<exception>, <result>), per-
        callee tuple.
        """
        self.wire_three_callables_2nd_one_failing()
        result = self.w.this()
        self.assert_result_wire_three_callables_2nd_one_failing(result)


    def test_wire_force_coupled_call(self):
        """
        Wire a callable, call it forcing coupling.
        """
        self.wire_returns_42_callable()
        result = self.w.couple.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_wire_wire_coupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.wire_three_callables_2nd_one_failing()
        with self.assertRaises(RuntimeError) as cm:
            self.w.couple.this()
        self.assert_failure_wire_three_callables_2nd_one_failing(cm)


    def test_wire_force_decoupled_call(self):
        """
        Wire a callable, call it forcing coupling.
        """
        self.wire_returns_42_callable()
        result = self.w.decouple.this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_wire_wire_decoupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.wire_three_callables_2nd_one_failing()
        result = self.w.decouple.this()
        self.assert_result_wire_three_callables_2nd_one_failing(result)


# ----------------------------------------------------------------------------
