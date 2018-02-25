# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import logging
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



class TestWiresCalleeFailures(unittest.TestCase):

    """
    Callee failure tests using the Wires singleton.
    """

    def setUp(self):

        wire.will_fail.calls_to(self._failing_callee)
        self.addCleanup(unwire.will_fail.calls_to, self._failing_callee)


    _THE_EXCEPTION = RuntimeError('something bad')


    def _failing_callee(self):

        raise self._THE_EXCEPTION


    def test_logs_error(self):

        log_handler = helpers.TrackingLoggingHandler()
        root_logger = logging.getLogger()
        root_logger.addHandler(log_handler)

        wire.will_fail()

        # We get two log records:
        # - The first one with a "custom" call fail record.
        # - The second with the triggering exception + traceback record.
        self.assertEqual(len(log_handler.records), 2, 'logged record count')

        record = log_handler.records[0]
        self.assertTrue(
            record.msg.startswith(repr('will_fail')),
            'first log record does not start with wires callable repr',
        )
        self.assertIn(
            self._failing_callee.__name__,
            record.msg,
            'first log record does not contain failing callee name',
        )
        self.assertIn(
            repr(self._THE_EXCEPTION),
            record.msg,
            'first log record does not contain callee exception repr',
        )
        self.assertEqual(
            record.levelname,
            'ERROR',
            'first log record level name',
        )
        self.assertIs(
            record.exc_info,
            None,
            'first log record exception info'
        )

        record = log_handler.records[1]
        self.assertIs(
            record.msg,
            self._THE_EXCEPTION,
            'second log record mismatched message',
        )
        self.assertEqual(
            record.levelname,
            'ERROR',
            'second log record level name',
        )
        self.assertIsInstance(
            record.exc_info,
            tuple,
            'second log record exception info type'
        )
        self.assertEqual(
            len(record.exc_info),
            3,
            'second log record exception info length'
        )
        self.assertIs(
            record.exc_info[0],
            RuntimeError,
            'second log record exception info type'
        )
        self.assertIs(
            record.exc_info[1],
            self._THE_EXCEPTION,
            'second log record exception info value'
        )
        # There must be a better way of confirming this is a traceback object!
        for tb_attr in ('tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next'):
            self.assertTrue(
                getattr(record.exc_info[2], tb_attr, None),
                'second log record traceback with no %r attribute' % (tb_attr,) 
            )


# ----------------------------------------------------------------------------
