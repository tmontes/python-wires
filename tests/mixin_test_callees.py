# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Test callees mixin.
"""


from __future__ import absolute_import

from . import helpers



class TestCalleesMixin(object):

    """
    Holds test callees.
    """

    @staticmethod
    def returns_42_callee():

        return 42


    @staticmethod
    def returns_None_callee():

        return None


    THE_EXCEPTION = ValueError('bad value detail')

    def raises_exception_callee(self):

        raise self.THE_EXCEPTION


    def unwire_call(self, callee):

        self.unwire.this.calls_to(callee)


# ----------------------------------------------------------------------------
