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
    Wiring and Assertion mixin for caller/callee call-time coupling tests.
    """

    def wire_returns_42_callable(self):
        """
        Wire `TestCallablesMixin.returns_42_callable` to self.w.this.
        """
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.w.this.unwire, self.returns_42_callable)


    def assert_result_wire_returns_42_callable(self, result):

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def wire_raises_exeption_callable(self):
        """
        Wire `TestCallablesMixin.raises_exception_callable` to self.w.this.
        """
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
        """
        Wire three `TestCallablesMixin.*` callables to self.w.this, where the
        2nd one raises an exception, when called.
        """
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
    Drives Wires caller/callee coupling tests.
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
        result = self.w(coupling=True).this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_wire_wire_coupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.wire_three_callables_2nd_one_failing()
        with self.assertRaises(RuntimeError) as cm:
            self.w(coupling=True).this()
        self.assert_failure_wire_three_callables_2nd_one_failing(cm)


    def test_wire_force_decoupled_call(self):
        """
        Wire a callable, call it with no coupling.
        """
        self.wire_returns_42_callable()
        result = self.w(coupling=False).this()
        self.assert_result_wire_returns_42_callable(result)


    def test_wire_wire_wire_decoupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.wire_three_callables_2nd_one_failing()
        result = self.w(coupling=False).this()
        self.assert_result_wire_three_callables_2nd_one_failing(result)


# ----------------------------------------------------------------------------
