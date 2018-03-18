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


    def test_wiring_repr(self):
        """
        Looks like an instantiation call, which should work.
        """
        repr_str = repr(self.w)
        self.assertTrue(repr_str.startswith('Wiring('), 'bad repr start')
        self.assertTrue(repr_str.endswith(')'), 'bad repr end')

        from wires import Wiring
        eval(repr_str)


    def test_callable_repr(self):
        """
        Between angle brackets, contains callable name repr.
        """
        self.w.callable_name.wire(self.returns_42)
        self.addCleanup(self.w.callable_name.unwire, self.returns_42)

        repr_str = repr(self.w.callable_name)
        self.assertTrue(repr_str.startswith('<WiringCallable '), 'bad repr start')
        self.assertTrue(repr_str.endswith('>'), 'bad repr end')
        self.assertTrue(repr('callable_name') in repr_str, 'no name in repr')


    def test_del_unknown_callable_attr_raises_attribute_error(self):
        """
        Deleting an unknown Callable attribute raises AttributeError.
        """
        with self.assertRaises(AttributeError) as cm:
            del self.w.this.no_such_attribute

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'no_such_attribute')


    def test_setgetdel_unknown_callable_attribute_works(self):
        """
        Can set, get and del random Callable attributes: as expected.
        """
        with self.assertRaises(AttributeError):
            _ = self.w.this.no_such_attribute

        self.w.this.no_such_attribute = 2
        self.assertEqual(self.w.this.no_such_attribute, 2)
        del self.w.this.no_such_attribute

        with self.assertRaises(AttributeError):
            _ = self.w.this.no_such_attribute


    def test_callable_setattr_delattr(self):
        """
        Deleting a Callable attribute reverts its value to its instance's value.
        """
        defaults = {
            'min_wirings': (None, 1),
            'max_wirings': (None, 1),
            'returns': (False, True),
            'ignore_failures': (True, False),
        }
        for attr_name, (default_value, test_value) in defaults.items():
            value = getattr(self.w.this, attr_name)
            self.assertEqual(
                value,
                default_value,
                'starting %s should be %r' % (attr_name, default_value),
            )

            setattr(self.w.this, attr_name, test_value)
            value = getattr(self.w.this, attr_name)
            self.assertEqual(value, test_value)

            delattr(self.w.this, attr_name)
            value = getattr(self.w.this, attr_name)
            self.assertEqual(
                value,
                default_value,
                'final %s should be %r' % (attr_name, default_value),
            )


    def test_callable_set(self):
        """
        Exercises the Callable's .set method.
        """
        # Set multiple settings on the `this` callable.
        self.w.this.set(
            min_wirings=1,
            max_wirings=1,
            returns=True,
            ignore_failures=False,
        )

        # Calling it raises an exception: min_wirings=1 but no wirings.
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()
        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'less than min_wirings wired')

        # Wire one callable.
        self.w.this.wire(self.raises_exception)
        self.addCleanup(self.w.this.unwire, self.raises_exception)

        # Calling it raises a different exception: returns + ignore_failures
        with self.assertRaises(RuntimeError) as cm:
            _ = self.w.this()
        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        # (<callee-exception>, None) are the exception's arguments.
        exception, result = exception_args[0]
        self.assertIsInstance(exception, ValueError)
        self.assertEqual(len(exception.args), 1)
        self.assertEqual(exception.args[0], 'test exception value error message')
        self.assertIsNone(result)

        # Need to set min_wirings back to None such that cleanup does not fail.
        self.w.this.set(min_wirings=None)


# ----------------------------------------------------------------------------
