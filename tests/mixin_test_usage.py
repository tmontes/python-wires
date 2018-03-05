# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

from . import helpers



class TestWiresUsageMixin(helpers.CallTrackerAssertMixin):

    """
    Drives Wires usage tests requiring mixed class to:
    - Have a Wiring instance at self.w.
    - Allow wiring via self.wire.
    - Allow unwiring via self.unwire.
    """

    def test_wire_call(self):
        """
        Wires the `this` call and calls it.
        Checks the wired callable was called once with the correct arguments.
        """
        tracker = helpers.CallTracker()

        self.wire.this.calls_to(tracker)
        self.w.this()

        self.assertEqual(tracker.call_count, 1, 'call count mismatch')
        self.assertEqual(tracker.call_args, [
            ((), {},),
        ], 'call argument mismatch')


    def test_double_wire_call(self):
        """
        Wires the `this` call twice and calls it.
        Checks the wired callable was called twice with the correct arguments.
        """
        tracker = helpers.CallTracker()

        self.wire.this.calls_to(tracker)
        self.wire.this.calls_to(tracker)
        self.w.this()

        self.assertEqual(tracker.call_count, 2, 'call count mismatch')
        self.assertEqual(tracker.call_args, [
            ((), {},),
            ((), {},),
        ], 'call argument mismatch')


    def test_multi_wired_call(self):
        """
        Wires the `this` call to multiple callables and calls it.
        Checks that each of the wired callables was called once with the correct
        arguments.
        """
        num_wirings = 10

        trackers = [helpers.CallTracker() for _ in range(num_wirings)]

        for tracker in trackers:
            self.wire.this.calls_to(tracker)

        self.w.this()

        for tracker in trackers:
            self.assertEqual(tracker.call_count, 1, 'call count mismatch')
            self.assertEqual(tracker.call_args, [
                ((), {},),
            ], 'call argument mismatch')


    def test_wire_call_unwire_call(self):
        """
        Wires the `this` call to a callable and calls it.
        Checks the wired callable was called once with the correct arguments.
        Unwires the `this` callable and calls it again.
        Checks the wired callable wasn't called again.
        """
        tracker = helpers.CallTracker()

        self.wire.this.calls_to(tracker)
        self.w.this()

        self.assert_single_call_no_args(tracker)

        self.unwire.this.calls_to(tracker)
        self.w.this()

        self.assert_single_call_no_args(tracker)


# ----------------------------------------------------------------------------
