# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
API test driver mixin.
"""


from __future__ import absolute_import

from . import mixin_test_callables



class TestWiresAPIMixin(mixin_test_callables.TestCallablesMixin):

    """
    Drives Wires API tests.

    Requires the mixed class provide a Wires instance at `self.w`.
    """

    def test_unwired_call_does_not_fail(self):
        """
        Calling an unwired call works. Does nothing, but works.
        """
        self.w.unwired_call()


    def test_wiring_non_callable_raises_type_error(self):
        """
        Wiring a call to a non-callable raises TypeError.
        The exception argument (message):
        - Starts with "argument not callable: ".
        - Contains repr(argument).
        """
        for non_callable in (None, True, 42, 2.3, (), [], {}, set()):

            with self.assertRaises(TypeError) as cm:
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


    def test_unwiring_non_callable_raises_type_error(self):
        """
        Unwiring a call from a non-callable raises TypeError.
        The exception argument (message):
        - Starts with "argument not callable: ".
        - Contains repr(argument).
        """
        for non_callable in (None, True, 42, 2.3, (), [], {}, set()):

            with self.assertRaises(TypeError) as cm:
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


    def test_wiring_with_args_and_plain_unwiring_works(self):
        """
        Unwiring a plain callable after wiring it with wire-time args works.
        """
        self.w.this.wire(self.returns_42, 42, value=42)
        self.w.this.unwire(self.returns_42)

        # len(callable) is the number of wirings
        self.assertEqual(len(self.w.this), 0)


    def test_unwiring_matching_args_works(self):
        """
        Unwiring with args unwires the matching wiring and raises ValueError
        if no wirings with such wire-time args are found.
        """
        self.w.this.wire(self.returns_42, 42, value=42)
        self.w.this.wire(self.returns_42, 24, value=24)

        # unwires the 2nd wiring: should work
        self.w.this.unwire(self.returns_42, 24, value=24)

        # assert one wiring
        wirings = self.w.this.wirings
        self.assertEqual(len(wirings), 1)

        # assert we're left with the correct wiring/wire-time args
        func, args, kwargs = wirings[0]
        self.assertIs(func, self.returns_42)
        self.assertEqual(args, (42,))
        self.assertEqual(kwargs, {'value': 42})

        # this wiring is now gone, should raise
        with self.assertRaises(ValueError):
            self.w.this.unwire(self.returns_42, 24, value=24)

        # no such wire-time positional/named args, should raise
        with self.assertRaises(ValueError):
            self.w.this.unwire(self.returns_42, 'nswtpa', value='nswtna')

        # unwire the 1st wiring, matching these wire-time args
        self.w.this.unwire(self.returns_42, 42, value=42)

        # assert no wirings
        self.assertEqual(len(self.w.this), 0)



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
            msg.startswith('non-wired function '),
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
        Iterating over a Wires instance produces its callables.
        """
        self.w.callable1.wire(self.returns_42)
        self.w.callable2.wire(self.returns_none)
        self.addCleanup(self.w.callable1.unwire, self.returns_42)
        self.addCleanup(self.w.callable2.unwire, self.returns_none)

        created_callables = set((self.w.callable1, self.w.callable2))
        obtained_callables = set(self.w)

        self.assertEqual(created_callables, obtained_callables)


    def test_wires_object_dir_callables(self):
        """
        Callable names are present in a Wires object's dir() output.
        """
        self.w.callable1.wire(self.returns_42)
        self.w.callable2.wire(self.returns_none)
        self.addCleanup(self.w.callable1.unwire, self.returns_42)
        self.addCleanup(self.w.callable2.unwire, self.returns_none)

        dir_output = dir(self.w)
        self.assertIn('callable1', dir_output)
        self.assertIn('callable2', dir_output)


    def test_wires_object_dir_normal_attrs(self):
        """
        Regular attributes are present in a Wires object's dir() output.
        """
        self.w.attr1 = 42
        self.w.attr2 = 24

        dir_output = dir(self.w)
        self.assertIn('attr1', dir_output)
        self.assertIn('attr2', dir_output)


    def test_wires_object_dir_callables_and_normal_attrs(self):
        """
        All attribute names (callables or not) are present in a Wires object's
        dir() output.
        """
        self.w.callable1.wire(self.returns_42)
        self.w.callable2.wire(self.returns_none)
        self.addCleanup(self.w.callable1.unwire, self.returns_42)
        self.addCleanup(self.w.callable2.unwire, self.returns_none)

        self.w.attr1 = 42
        self.w.attr2 = 24

        dir_output = dir(self.w)
        self.assertIn('callable1', dir_output)
        self.assertIn('callable2', dir_output)
        self.assertIn('attr1', dir_output)
        self.assertIn('attr2', dir_output)


    def test_wires_object_len(self):
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


    def test_wires_object_repr(self):
        """
        Looks like an instantiation call, which should work.
        """
        repr_str = repr(self.w)
        self.assertTrue(repr_str.startswith('Wires('), 'bad repr start')
        self.assertTrue(repr_str.endswith(')'), 'bad repr end')

        from wires import Wires
        eval(repr_str)


    def test_callable_repr(self):
        """
        Between angle brackets, contains callable name repr and id(self).
        """
        self.w.callable_name.wire(self.returns_42)
        self.addCleanup(self.w.callable_name.unwire, self.returns_42)

        repr_str = repr(self.w.callable_name)
        self.assertTrue(repr_str.startswith('<WiresCallable '), 'bad repr start')
        self.assertTrue(repr('callable_name') in repr_str, 'no name in repr')
        ending = ' at 0x%x>' % id(self.w.callable_name)
        self.assertTrue(repr_str.endswith(ending), 'bad repr end')


    def test_wires_object_set_del_regular_attr_works(self):
        """
        Setting a Wires attribute to something, then deleting it, then
        accessing it, creates a "normal" callable object, as expected.
        """
        self.w.what_for = 42
        self.assertEqual(self.w.what_for, 42)

        del self.w.what_for
        self.assertTrue(callable(self.w.what_for), 'non-callable attribute')


    def test_wires_object_del_nonsuch_attr_raises_attribute_error(self):
        """
        Deleting a non-existing Wires object attribute raises an AttributeError.
        """
        with self.assertRaises(AttributeError) as cm:
            del self.w.no_such_attribute

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertIn('no_such_attribute', exception_args[0])


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
            'ignore_exceptions': (True, False),
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
            ignore_exceptions=False,
        )

        # Calling it raises an exception: min_wirings=1 but no wirings.
        with self.assertRaises(ValueError) as cm:
            _ = self.w.this()
        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)
        self.assertEqual(exception_args[0], 'less than min_wirings wired')

        # Wire one callable.
        self.w.this.wire(self.raises_exception)
        self.addCleanup(self.w.this.unwire, self.raises_exception)

        # Calling it raises a different exception: returns + ignore_exceptions
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
