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

from . import mixin_test_callables



class TestWiresAPIMixin(mixin_test_callables.TestCallablesMixin):

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
                self.w.this.wire(non_callable)

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
                self.w.this.unwire(non_callable)

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
        self.w.this.wire(self.returns_42)
        self.addCleanup(self.w.this.unwire, self.returns_42)


    def test_wiring_unwiring_works(self):
        """
        Wiring and then unwiring same callable works.
        """
        self.w.this.wire(self.returns_42)
        self.w.this.unwire(self.returns_42)


    def test_unwiring_unknown_callable_raises_value_error(self):
        """
        Unwiring an unknown callable raises a ValueError.
        The exception argument (message):
        - Starts with "unknown function ".
        """
        with self.assertRaises(ValueError) as cm:
            self.w.this.unwire(self.returns_42)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)

        msg = exception_args[0]
        self.assertTrue(
            msg.startswith('unknown function '),
            'wrong exception message: %r' % (msg,),
        )


    def test_dynamic_name_wire_unwire_works(self):
        """
        Wiring/unwiring via indexing works.
        """
        name = 'name'
        self.w[name].wire(self.returns_42)
        self.w[name].unwire(self.returns_42)


    def test_create_and_delete_callable_works(self):
        """
        Creating and deleting a callable works.
        """
        self.w.this.wire(self.returns_42)
        del self.w.this


    def test_callables_have_names(self):
        """
        Created callables have a __name__ attribute matching their name.
        """
        self.w.this.wire(self.returns_42)
        self.addCleanup(self.w.this.unwire, self.returns_42)

        self.assertEqual(self.w.this.__name__, 'this')


    def test_callables_wiring_attribute(self):
        """
        Created callables have a `.wirings` attribute that is a list of
        (<wired-callable>, <wired-args-tuple>, <wired-kwargs-dict>).
        """
        self.w.this.wire(self.returns_42)
        self.addCleanup(self.w.this.unwire, self.returns_42)

        wirings = self.w.this.wirings

        self.assertEqual(len(wirings), 1)

        wired_callable, wired_args, wired_kwargs = wirings[0]
        self.assertIs(wired_callable, self.returns_42)
        self.assertIsInstance(wired_args, tuple)
        self.assertEqual(wired_args, ())
        self.assertIsInstance(wired_kwargs, dict)
        self.assertEqual(wired_kwargs, {})


    def test_iteration_works(self):
        """
        Iterating over a Wiring instance produces its callables.
        """
        self.w.callable1.wire(self.returns_42)
        self.w.callable2.wire(self.returns_none)
        self.addCleanup(self.w.callable1.unwire, self.returns_42)
        self.addCleanup(self.w.callable2.unwire, self.returns_none)

        created_callables = set((self.w.callable1, self.w.callable2))
        obtained_callables = set(self.w)

        self.assertEqual(created_callables, obtained_callables)


    def test_wiring_len(self):
        """
        No callables means len is 0.
        """
        self.assertEqual(len(self.w), 0)


    def test_wire_wiring_len(self):
        """
        Rich wiring and callable length tests.
        """
        self.w.callable1.wire(self.returns_42)
        self.addCleanup(self.w.callable1.unwire, self.returns_42)

        self.assertEqual(len(self.w), 1)
        self.assertEqual(len(self.w.callable1), 1)

        self.w.callable2.wire(self.returns_42)
        self.w.callable2.wire(self.returns_none)
        self.addCleanup(self.w.callable2.unwire, self.returns_42)
        self.addCleanup(self.w.callable2.unwire, self.returns_none)

        self.assertEqual(len(self.w), 2)
        self.assertEqual(len(self.w.callable1), 1)
        self.assertEqual(len(self.w.callable2), 2)

        del self.w.callable1
        self.assertEqual(len(self.w), 1)
        self.assertEqual(len(self.w.callable2), 2)


# ----------------------------------------------------------------------------
