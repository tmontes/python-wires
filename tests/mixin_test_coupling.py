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

from . import helpers



class TestCallerCalleeCouplingMixin(object):

    """
    Drives Wires caller/callee coupling tests requiring mixed class to:
    - Have a Wiring instance at self.w.
    - Allow wiring via self.wire.
    - Allow unwiring via self.unwire.
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

        self.unwire.this.calls_to(callee)


    def test_default_uncoupled_wire_call(self):
        """
        Default uncoupled test: return a list of (<exception>, <result>), per-
        callee tuple.
        """
        self.wire.this.calls_to(self._returns_42_callee)
        self.addCleanup(self._unwire_call, self._returns_42_callee)
        result = self.w.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_default_uncoupled_wire_wire_wire_call(self):
        """
        Default uncoupled test: return a list of (<exception>, <result>), per-
        callee tuple.
        """
        self.wire.this.calls_to(self._returns_42_callee)
        self.wire.this.calls_to(self._raises_exception_callee)
        self.wire.this.calls_to(self._returns_None_callee)
        self.addCleanup(self._unwire_call, self._returns_None_callee)
        self.addCleanup(self._unwire_call, self._raises_exception_callee)
        self.addCleanup(self._unwire_call, self._returns_42_callee)
        result = self.w.this()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], (None, 42))
        self.assertEqual(result[1], (self._THE_EXCEPTION, None))
        self.assertEqual(result[2], (None, None))


    def test_wire_force_coupled_call(self):
        """
        Wire a callable, call it forcing coupling.
        """
        self.wire.this.calls_to(self._returns_42_callee)
        self.addCleanup(self._unwire_call, self._returns_42_callee)
        result = self.w.coupled_call.this()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (None, 42))


    def test_wire_wire_wire_coupled_call(self):
        """
        Wire a callable three times: the second one raises an exception.
        """
        self.wire.this.calls_to(self._returns_42_callee)
        self.wire.this.calls_to(self._raises_exception_callee)
        self.wire.this.calls_to(self._returns_None_callee)
        self.addCleanup(self._unwire_call, self._returns_None_callee)
        self.addCleanup(self._unwire_call, self._raises_exception_callee)
        self.addCleanup(self._unwire_call, self._returns_42_callee)

        with self.assertRaises(RuntimeError) as cm:
            self.w.coupled_call.this()

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], [(None, 42)])


# ----------------------------------------------------------------------------
