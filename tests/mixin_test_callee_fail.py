# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import logging
import sys

import six

from . import helpers



class TestWiresCalleeFailMixin(object):

    """
    Drives Wires callee failure tests requiring mixed class to:
    - Have a Wiring instance at self.w.
    """

    def setUp(self):

        self.log_handler = helpers.TrackingLoggingHandler()
        self.root_logger = logging.getLogger()
        self.root_logger.addHandler(self.log_handler)

        self.stderr = six.StringIO()
        self._save_sys_stderr = sys.stderr
        sys.stderr = self.stderr

        self.wire.will_fail.calls_to(self._failing_callee)


    def tearDown(self):

        self.unwire.will_fail.calls_to(self._failing_callee)
        sys.stderr = self._save_sys_stderr
        self.root_logger.removeHandler(self.log_handler)


    _THE_EXCEPTION = RuntimeError('something bad')


    def _failing_callee(self):

        raise self._THE_EXCEPTION


    def test_callee_execption_logs_error(self):

        self.w.will_fail.use_log = True
        self.w.will_fail()

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
        self.w.will_fail.use_log = False
        self.w.will_fail()

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
        self.w.will_fail.use_log = None
        self.w.will_fail()

        # We get no log records.
        self.assertEqual(len(self.log_handler.records), 0, 'log record count')

        # We get no stderr output.
        self.assertEqual(self.stderr.getvalue(), '', 'stderr output')


# ----------------------------------------------------------------------------
