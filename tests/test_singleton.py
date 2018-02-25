# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from wires import wire, unwire

from . import helpers



class TestWiresAPI(unittest.TestCase):

    """
    Minimal API tests for the Wires singleton.
    """

    @staticmethod
    def test_unwired_call_does_not_fail():
        """
        Calling an unwired call works. Does nothing, but works.
        """
        wire.unwired_call()


    def test_wiring_non_callable_raises_value_error(self):
        """
        Wiring a call to a non-callable raises ValueError.
        The exception argument (message):
        - Starts with "argument not callable: ".
        - Contains repr(argument).
        """
        for non_callable in (None, True, 42, 2.3, (), [], {}, set()):

            with self.assertRaises(ValueError) as cm:
                wire.this.calls_to(non_callable)

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


    @staticmethod
    def test_wiring_callable_works():
        """
        Wiring a callable works.
        """
        wire.this.calls_to(lambda: None)


    @staticmethod
    def test_wiring_unwiring_works():
        """
        Wiring and then unwiring to the same callable works.
        """
        test_callable = lambda: None

        wire.this.calls_to(test_callable)
        unwire.this.calls_to(test_callable)


    def test_unwiring_unknown_callable_raises_value_error(self):
        """
        Unwiring an unknown callable raises a ValueError.
        The exception argument (message):
        - Starts with "unknown function ".
        """
        test_callable = lambda: None

        with self.assertRaises(ValueError) as cm:
            unwire.this.calls_to(test_callable)

        exception_args = cm.exception.args
        self.assertEqual(len(exception_args), 1)

        msg = exception_args[0]
        self.assertTrue(
            msg.startswith('unknown function '),
            'wrong exception message: %r' % (msg,),
        )



class TestWiresUtilization(helpers.CallTrackerAssertMixin, unittest.TestCase):

    """
    Utilization tests for the Wires singleton.
    """

    def test_wire_call(self):
        """
        Wires the `this` call and calls it.
        Checks the wired callable was called once with the correct arguments.
        """
        tracker = helpers.CallTracker()

        wire.this.calls_to(tracker)
        wire.this()

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

        wire.this.calls_to(tracker)
        wire.this.calls_to(tracker)
        wire.this()

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
            wire.this.calls_to(tracker)

        wire.this()

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

        wire.this.calls_to(tracker)
        wire.this()

        self.assert_single_call_no_args(tracker)

        unwire.this.calls_to(tracker)
        wire.this()

        self.assert_single_call_no_args(tracker)


# ----------------------------------------------------------------------------
