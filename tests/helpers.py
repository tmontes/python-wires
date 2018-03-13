# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires test helpers.
"""


from __future__ import absolute_import



class CallTracker(object):

    """
    Tracks calls to self.
    """

    def __init__(self, returns=None, raises=None):

        # Appended with (args, kwargs) on each call.
        self.call_args = []

        self._returns = returns
        self._raises = raises


    def __call__(self, *args, **kwargs):

        self.call_args.append((args, kwargs))
        if self._raises:
            raise self._raises
        return self._returns


    @property
    def call_count(self):
        """
        Calls to self count.
        """
        return len(self.call_args)


    def reset(self):
        """
        Reset ourselves.
        """
        self.call_args = []



class CallTrackerAssertMixin(object):

    """
    Call tracking assertion methods.
    """

    def assert_called(self, call_tracker, expected_call_arg_list):
        """
        Asserts `call_tracker` was called as many times as there are entries
        in `expected_call_arg_list` and that the arguments match.
        """
        self.assertEqual(
            call_tracker.call_count,
            len(expected_call_arg_list),
            'call count mismatch',
        )
        self.assertEqual(
            call_tracker.call_args,
            expected_call_arg_list,
            'call argument mismatch',
        )


    def assert_single_call_no_args(self, call_tracker):
        """
        Asserts `call_tracker` was called once, with no arguments.
        """
        expected_call_arg_list = [
            ((), {},),
        ]
        self.assert_called(call_tracker, expected_call_arg_list)


# ----------------------------------------------------------------------------
