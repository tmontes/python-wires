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

    def __init__(self):

        # Appended with (args, kwargs) on each call.
        self.call_args = []


    def __call__(self, *args, **kwargs):

        self.call_args.append((args, kwargs))


    @property
    def call_count(self):
        """
        Calls to self count.
        """
        return len(self.call_args)



class CallTrackerAssertMixin(object):

    def assert_called(self, call_tracker, expected_call_arg_list):

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


    def assert_single_call_no_args(self, tracker):

        expected_call_arg_list = [
            ((), {},),
        ]
        self.assert_called(tracker, expected_call_arg_list)


# ----------------------------------------------------------------------------
