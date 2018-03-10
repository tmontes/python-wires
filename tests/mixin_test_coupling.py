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



class TestCallerCalleeCouplingMixin(mixin_test_callables.TestCallablesMixin):

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
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_wire_wire_default_decoupled_call(self):
        """
        Default uncoupled test: return a list of (<exception>, <result>), per-
        callee tuple.
        """
        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.raises_exception_callable)
        self.w.this.wire(self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.raises_exception_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        result = self.w.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


    def test_wire_force_coupled_call(self):
        """
        Wire a callable, call it forcing coupling.
        """
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        result = self.w.couple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_wire_wire_coupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.raises_exception_callable)
        self.w.this.wire(self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.raises_exception_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)

        with self.assertRaises(RuntimeError) as cm:
            self.w.couple.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 2)
        self.assertEqual(exception_args[0], (None, 42))
        self.assertEqual(exception_args[1], (self.THE_EXCEPTION, None))


    def test_wire_force_decoupled_call(self):
        """
        Wire a callable, call it forcing coupling.
        """
        self.w.this.wire(self.returns_42_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)
        result = self.w.decouple.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_wire_wire_decoupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.w.this.wire(self.returns_42_callable)
        self.w.this.wire(self.raises_exception_callable)
        self.w.this.wire(self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.returns_None_callable)
        self.addCleanup(self.unwire_call, self.raises_exception_callable)
        self.addCleanup(self.unwire_call, self.returns_42_callable)

        result = self.w.decouple.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self.THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


# ----------------------------------------------------------------------------
