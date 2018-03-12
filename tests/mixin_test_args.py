# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Argument passing test driver mixin.
"""


from __future__ import absolute_import

from . import helpers, mixin_test_callables



class _TestWiresArgPassingMixin(mixin_test_callables.TestCallablesMixin,
                                helpers.CallTrackerAssertMixin):

    """
    Argument passing utilization tests for the shared Wiring instance.
    """

    wire1_args = ()
    wire1_kwargs = {}

    wire2_args = ()
    wire2_kwargs = {}

    call_args = ()
    call_kwargs = {}


    def test_wire_call_args(self):
        """
        Wires the `this` call and calls it.
        Checks the wired callable was called once with the correct arguments.
        """
        tracker = helpers.CallTracker()

        self.w.this.wire(tracker, *self.wire1_args, **self.wire1_kwargs)
        self.w.this(*self.call_args, **self.call_kwargs)
        self.addCleanup(self.w.this.unwire, tracker)

        self.assertEqual(tracker.call_count, 1, 'call count mismatch')
        self.assertEqual(tracker.call_args, [
            (self.expected_call_args, self.expected_call_kwargs),
        ], 'call argument mismatch')


    def test_double_wire_call_args(self):
        """
        Wires the `this` call and calls it.
        Checks the wired callable was called once with the correct arguments.
        """
        tracker = helpers.CallTracker()

        self.w.this.wire(tracker, *self.wire1_args, **self.wire1_kwargs)
        self.w.this.wire(tracker, *self.wire2_args, **self.wire2_kwargs)
        self.w.this(*self.call_args, **self.call_kwargs)
        self.addCleanup(self.w.this.unwire, tracker)
        self.addCleanup(self.w.this.unwire, tracker)

        self.assertEqual(tracker.call_count, 2, 'call count mismatch')
        self.assertEqual(tracker.call_args, [
            (self.expected_call_args, self.expected_call_kwargs),
            (self.expected_2nd_call_args, self.expected_2nd_call_kwargs),
        ], 'call argument mismatch')



class TestWiresNoArgPassingMixin(_TestWiresArgPassingMixin):

    """
    No wire-time args/kwargs, no call-time args/kwargs.
    """

    expected_call_args = ()
    expected_call_kwargs = {}

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireArgPassingMixin(_TestWiresArgPassingMixin):

    """
    Wire-time args, no call-time args/kwargs.
    """

    wire1_args = (1, 2, 3)

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = {}

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireKwargPassingMixin(_TestWiresArgPassingMixin):

    """
    Wire-time kwargs, no call-time args/kwargs.
    """

    wire1_kwargs = dict(a='a', b='b')

    expected_call_args = ()
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireArgKwargPassingMixin(_TestWiresArgPassingMixin):

    """
    Wire-time args and kwargs, no call-time args/kwargs.
    """

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresCallArgPassingMixin(_TestWiresArgPassingMixin):

    """
    No wire-time args/kwargs, call-time args.
    """

    call_args = (1, 2, 3)

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = {}

    expected_2nd_call_args = (1, 2, 3)
    expected_2nd_call_kwargs = {}



class TestWiresCallKwargPassingMixin(_TestWiresArgPassingMixin):

    """
    No wire-time args/kwargs, call-time kwargs.
    """

    call_kwargs = dict(a='a', b='b')

    expected_call_args = ()
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = dict(a='a', b='b')



class TestWiresCallArgKwargPassingMixin(_TestWiresArgPassingMixin):

    """
    No wire-time args/kwargs, call-time wire args and kwargs.
    """

    call_args = (1, 2, 3)
    call_kwargs = dict(a='a', b='b')

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = (1, 2, 3)
    expected_2nd_call_kwargs = dict(a='a', b='b')



class TestWiresFullPassingMixin(_TestWiresArgPassingMixin):

    """
    Wire-time args and kwargs, call-time args and kwargs.
    """

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    call_args = (4, 5, 6)
    call_kwargs = dict(c='c', d='d')

    expected_call_args = (1, 2, 3, 4, 5, 6)
    expected_call_kwargs = dict(a='a', b='b', c='c', d='d')

    expected_2nd_call_args = (4, 5, 6)
    expected_2nd_call_kwargs = dict(c='c', d='d')



class TestWiresDoubleFullPassingMixin(_TestWiresArgPassingMixin):

    """
    Two wirings with separate args and kwargs each, call time arg and kwargs.
    """

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    wire2_args = (4, 5, 6)
    wire2_kwargs = dict(c='c', d='d')

    call_args = (7, 8, 9)
    call_kwargs = dict(e='e', f='f')

    expected_call_args = (1, 2, 3, 7, 8, 9)
    expected_call_kwargs = dict(a='a', b='b', e='e', f='f')

    expected_2nd_call_args = (4, 5, 6, 7, 8, 9)
    expected_2nd_call_kwargs = dict(c='c', d='d', e='e', f='f')


# ----------------------------------------------------------------------------
