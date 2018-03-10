# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Test callables mixin.
"""


from __future__ import absolute_import

from . import helpers



class TestCallablesMixin(object):

    """
    Holds test callables.
    """

    @staticmethod
    def returns_42_callable():

        return 42


    @staticmethod
    def returns_None_callable():

        return None


    THE_EXCEPTION = ValueError('bad value detail')

    def raises_exception_callable(self):

        raise self.THE_EXCEPTION


    def unwire_call(self, callable_):

        self.w.this.unwire(callable_)


# ----------------------------------------------------------------------------
