# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import logging
import unittest
import sys

import six

from wires import Wires

from . import helpers



class TestWiresAPI(unittest.TestCase):

    """
    Minimal API tests for the Wires singleton.
    """

    def setUp(self):

        self.wires = Wires()


    def test_unwired_call_does_not_fail(self):
        """
        Calling an unwired call works. Does nothing, but works.
        """
        self.wires.wire.unwired_call()


    def test_wiring_non_callable_raises_value_error(self):
        """
        Wiring a call to a non-callable raises ValueError.
        The exception argument (message):
        - Starts with "argument not callable: ".
        - Contains repr(argument).
        """
        for non_callable in (None, True, 42, 2.3, (), [], {}, set()):

            with self.assertRaises(ValueError) as cm:
                self.wires.wire.this.calls_to(non_callable)

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
        test_callable = lambda: None
        
        # Calling test_callble works (for coverage completion's sake).
        test_callable()

        self.wires.wire.this.calls_to(test_callable)


    def test_wiring_unwiring_works(self):
        """
        Wiring and then unwiring to the same callable works.
        """
        test_callable = lambda: None

        # Calling test_callble works (for coverage completion's sake).
        test_callable()

        self.wires.wire.this.calls_to(test_callable)
        self.wires.unwire.this.calls_to(test_callable)


    def test_unwiring_unknown_callable_raises_value_error(self):
        """
        Unwiring an unknown callable raises a ValueError.
        The exception argument (message):
        - Starts with "unknown function ".
        """
        test_callable = lambda: None

        # Calling test_callble works (for coverage completion's sake).
        test_callable()

        with self.assertRaises(ValueError) as cm:
            self.wires.unwire.this.calls_to(test_callable)

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

    def setUp(self):

        self.wires = Wires()


    def test_wire_call(self):
        """
        Wires the `this` call and calls it.
        Checks the wired callable was called once with the correct arguments.
        """
        tracker = helpers.CallTracker()

        self.wires.wire.this.calls_to(tracker)
        self.wires.this()

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

        self.wires.wire.this.calls_to(tracker)
        self.wires.wire.this.calls_to(tracker)
        self.wires.this()

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
            self.wires.wire.this.calls_to(tracker)

        self.wires.this()

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

        self.wires.wire.this.calls_to(tracker)
        self.wires.this()

        self.assert_single_call_no_args(tracker)

        self.wires.unwire.this.calls_to(tracker)
        self.wires.this()

        self.assert_single_call_no_args(tracker)



class TestWiresCalleeFailures(unittest.TestCase):

    """
    Callee failure tests using the Wires singleton.
    """

    def setUp(self):

        self.log_handler = helpers.TrackingLoggingHandler()
        self.root_logger = logging.getLogger()
        self.root_logger.addHandler(self.log_handler)

        self.stderr = six.StringIO()
        self._save_sys_stderr = sys.stderr
        sys.stderr = self.stderr

        self.wires = Wires()
        self.wires.wire.will_fail.calls_to(self._failing_callee)


    def tearDown(self):

        self.wires.unwire.will_fail.calls_to(self._failing_callee)
        sys.stderr = self._save_sys_stderr
        self.root_logger.removeHandler(self.log_handler)


    _THE_EXCEPTION = RuntimeError('something bad')


    def _failing_callee(self):

        raise self._THE_EXCEPTION


    def test_callee_execption_logs_error(self):

        self.wires.will_fail.use_log = True
        self.wires.will_fail()

        # We get two log records:
        # - The first one with a "custom" call fail record.
        # - The second with the triggering exception + traceback record.
        self.assertEqual(len(self.log_handler.records), 2, 'logged record count')

        record = self.log_handler.records[0]
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

        record = self.log_handler.records[1]
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


    def test_callee_execption_to_stderr(self):
        """
        Directs callee exceptions to stderr.
        No records logged at all.
        Failure is output to sys.stderr.
        """
        self.wires.will_fail.use_log = False
        self.wires.will_fail()

        # We get no log records.
        self.assertEqual(len(self.log_handler.records), 0, 'logged record count')

        # We get informative output on sys.stderr.
        stderr_value = self.stderr.getvalue()
        self.assertTrue(
            stderr_value.startswith(repr('will_fail')),
            'stderr does not start with wires callable repr',
        )
        self.assertIn(
            self._failing_callee.__name__,
            stderr_value,
            'stderr does not contain failing callee name',
        )
        self.assertIn(
            repr(self._THE_EXCEPTION),
            stderr_value,
            'stderr does not contain callee exception repr',
        )

        self.assertIn(
            'Traceback',
            stderr_value,
            'stderr does not contain traceback',
        )
        self.assertIn(
            'File',
            stderr_value,
            'stderr does not contain traceback',
        )


    def test_callee_execption_muted(self):
        """
        Directs callee exception reporting.
        No records logged at all.
        No output to sys.stderr.
        """
        self.wires.will_fail.use_log = None
        self.wires.will_fail()

        # We get no log records.
        self.assertEqual(len(self.log_handler.records), 0, 'log record count')

        # We get no stderr output.
        self.assertEqual(self.stderr.getvalue(), '', 'stderr output')


# ----------------------------------------------------------------------------
