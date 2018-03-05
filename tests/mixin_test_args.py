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

from . import helpers



class TestWiresArgPassingMixin(helpers.CallTrackerAssertMixin):

    """
    Argument passing utilization tests for the Wires singleton.
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

        self.wire.this.calls_to(tracker, *self.wire1_args, **self.wire1_kwargs)
        self.w.this(*self.call_args, **self.call_kwargs)
        self.addCleanup(self._unwire, tracker)

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

        self.wire.this.calls_to(tracker, *self.wire1_args, **self.wire1_kwargs)
        self.wire.this.calls_to(tracker, *self.wire2_args, **self.wire2_kwargs)
        self.w.this(*self.call_args, **self.call_kwargs)
        self.addCleanup(self._unwire, tracker)
        self.addCleanup(self._unwire, tracker)

        self.assertEqual(tracker.call_count, 2, 'call count mismatch')
        self.assertEqual(tracker.call_args, [
            (self.expected_call_args, self.expected_call_kwargs),
            (self.expected_2nd_call_args, self.expected_2nd_call_kwargs),
        ], 'call argument mismatch')


    def _unwire(self, tracker):

        self.unwire.this.calls_to(tracker)


# ----------------------------------------------------------------------------
