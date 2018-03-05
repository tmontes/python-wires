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

from wires import wiring, wire, unwire

from . import helpers



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

        wire.will_fail.calls_to(self._failing_callee)


    def tearDown(self):

        unwire.will_fail.calls_to(self._failing_callee)
        sys.stderr = self._save_sys_stderr
        self.root_logger.removeHandler(self.log_handler)


    _THE_EXCEPTION = RuntimeError('something bad')


    def _failing_callee(self):

        raise self._THE_EXCEPTION


    def test_callee_execption_logs_error(self):
        """
        Callee exceptions are logged by default.
        No output to sys.stderr should be produced.
        """
        wiring.will_fail.use_log = True
        wiring.will_fail()

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

        # Finally, check no output to stderr was produced.
        self.assertEqual(self.stderr.getvalue(), '')


    def test_callee_execption_to_stderr(self):
        """
        Directs callee exceptions to stderr.
        No records logged at all.
        Failure is output to sys.stderr.
        """
        wiring.will_fail.use_log = False
        wiring.will_fail()

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
        wiring.will_fail.use_log = None
        wiring.will_fail()

        # We get no log records.
        self.assertEqual(len(self.log_handler.records), 0, 'log record count')

        # We get no stderr output.
        self.assertEqual(self.stderr.getvalue(), '', 'stderr output')



class ArgPassingMixin(helpers.CallTrackerAssertMixin):

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

        wire.this.calls_to(tracker, *self.wire1_args, **self.wire1_kwargs)
        wiring.this(*self.call_args, **self.call_kwargs)
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

        wire.this.calls_to(tracker, *self.wire1_args, **self.wire1_kwargs)
        wire.this.calls_to(tracker, *self.wire2_args, **self.wire2_kwargs)
        wiring.this(*self.call_args, **self.call_kwargs)
        self.addCleanup(self._unwire, tracker)
        self.addCleanup(self._unwire, tracker)

        self.assertEqual(tracker.call_count, 2, 'call count mismatch')
        self.assertEqual(tracker.call_args, [
            (self.expected_call_args, self.expected_call_kwargs),
            (self.expected_2nd_call_args, self.expected_2nd_call_kwargs),
        ], 'call argument mismatch')


    def _unwire(self, tracker):

        unwire.this.calls_to(tracker)



class TestWiresNoArgPassing(ArgPassingMixin, unittest.TestCase):

    expected_call_args = ()
    expected_call_kwargs = {}

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireArgPassing(ArgPassingMixin, unittest.TestCase):

    wire1_args = (1, 2, 3)

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = {}

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireKwargPassing(ArgPassingMixin, unittest.TestCase):

    wire1_kwargs = dict(a='a', b='b')

    expected_call_args = ()
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireArgKwargPassing(ArgPassingMixin, unittest.TestCase):

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresCallArgPassing(ArgPassingMixin, unittest.TestCase):

    call_args = (1, 2, 3)

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = {}

    expected_2nd_call_args = (1, 2, 3)
    expected_2nd_call_kwargs = {}



class TestWiresCallKwargPassing(ArgPassingMixin, unittest.TestCase):

    call_kwargs = dict(a='a', b='b')

    expected_call_args = ()
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = dict(a='a', b='b')



class TestWiresCallArgKwargPassing(ArgPassingMixin, unittest.TestCase):

    call_args = (1, 2, 3)
    call_kwargs = dict(a='a', b='b')

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = (1, 2, 3)
    expected_2nd_call_kwargs = dict(a='a', b='b')



class TestWiresFullPassing(ArgPassingMixin, unittest.TestCase):

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    call_args = (4, 5, 6)
    call_kwargs = dict(c='c', d='d')

    expected_call_args = (1, 2, 3, 4, 5, 6)
    expected_call_kwargs = dict(a='a', b='b', c='c', d='d')

    expected_2nd_call_args = (4, 5, 6)
    expected_2nd_call_kwargs = dict(c='c', d='d')



class TestWiresDoubleFullPassing(ArgPassingMixin, unittest.TestCase):

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
