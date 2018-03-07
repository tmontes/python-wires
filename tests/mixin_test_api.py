# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
API test driver mixin.
"""


from __future__ import absolute_import

from . import mixin_test_callees



class TestWiresAPIMixin(mixin_test_callees.TestCalleesMixin):

    """
    Drives Wires API tests requiring mixed class to:
    - Have a Wiring instance at self.w.
    - Allow wiring via self.wire.
    - Allow unwiring via self.unwire.
    """

    def test_unwired_call_does_not_fail(self):
        """
        Calling an unwired call works. Does nothing, but works.
        """
        self.w.unwired_call()


    def test_wiring_non_callable_raises_value_error(self):
        """
        Wiring a call to a non-callable raises ValueError.
        The exception argument (message):
        - Starts with "argument not callable: ".
        - Contains repr(argument).
        """
        for non_callable in (None, True, 42, 2.3, (), [], {}, set()):

            with self.assertRaises(ValueError) as cm:
                self.wire.this.calls_to(non_callable)

            exception_args = cm.exception.args
            self.assertEqual(len(exception_args), 1)

            msg = exception_args[0]
            self.assertTrue(
                msg.startswith('argument not callable: '),
                'wrong exception message: %r' % (msg,),
            )
            self.assertIn(
                repr(non_callable),
                msg,
                'missing argument repr in message: %r' % (msg,),
            )


    def test_unwiring_non_callable_raises_value_error(self):
        """
        Unwiring a call from a non-callable raises ValueError.
        The exception argument (message):
        - Starts with "argument not callable: ".
        - Contains repr(argument).
        """
        for non_callable in (None, True, 42, 2.3, (), [], {}, set()):

            with self.assertRaises(ValueError) as cm:
                self.unwire.this.calls_to(non_callable)

            exception_args = cm.exception.args
            self.assertEqual(len(exception_args), 1)

            msg = exception_args[0]
            self.assertTrue(
                msg.startswith('argument not callable: '),
                'wrong exception message: %r' % (msg,),
            )
            self.assertIn(
                repr(non_callable),
                msg,
                'missing argument repr in message: %r' % (msg,),
            )


    def test_wiring_callable_works(self):
        """
        Wiring a callable works.
        """
        self.wire.this.calls_to(self.returns_42_callee)
        self.addCleanup(self.unwire_call, self.returns_42_callee)


    def test_wiring_unwiring_works(self):
        """
        Wiring and then unwiring same callable works.
        """
        self.wire.this.calls_to(self.returns_42_callee)
        self.unwire.this.calls_to(self.returns_42_callee)


    def test_unwiring_unknown_callable_raises_value_error(self):
        """
        Unwiring an unknown callable raises a ValueError.
        The exception argument (message):
        - Starts with "unknown function ".
        """
        with self.assertRaises(ValueError) as cm:
            self.unwire.this.calls_to(self.returns_42_callee)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)

        msg = exception_args[0]
        self.assertTrue(
            msg.startswith('unknown function '),
            'wrong exception message: %r' % (msg,),
        )


    def test_dynamic_name_wire_unwire(self):
        """
        Wiring/unwiring via indexing works.
        """
        name = 'name'
        self.wire[name].calls_to(self.returns_42_callee)
        self.unwire[name].calls_to(self.returns_42_callee)


    def _assert_exception_arg(self, cm, expected):

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], expected)


    def test_call_via_wire_fails(self):
        """
        Calling within wiring context raises a RuntimeError.
        """
        with self.assertRaises(RuntimeError) as cm:
            self.wire.some_callable()

        self._assert_exception_arg(cm, 'calling within wiring context')


    def test_call_via_unwire_fails(self):
        """
        Calling within unwiring context raises a RuntimeError.
        """
        with self.assertRaises(RuntimeError) as cm:
            self.unwire.some_callable()

        self._assert_exception_arg(cm, 'calling within wiring context')


    def test_wiring_from_instance_fails(self):
        """
        Wiring at the instance level raises RuntimeError.
        """
        with self.assertRaises(RuntimeError) as cm:
            self.w.some_callable.calls_to(self.returns_42_callee)

        self._assert_exception_arg(cm, 'undefined wiring context')


# ----------------------------------------------------------------------------
