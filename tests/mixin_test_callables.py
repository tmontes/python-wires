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



class TestCallablesMixin(object):

    """
    Holds test callables.
    """

    @staticmethod
    def returns_42_callable():
        """
        Answer to the Ultimate Question of Life, the Universe, and Everything.
        """
        return 42


    @staticmethod
    def returns_none_callable():
        """
        Zero, zip, zilch, nada.
        """
        return None


    THE_EXCEPTION = ValueError('bad value detail')

    def raises_exception_callable(self):
        """
        I love the smell of napalm in the morning.
        """
        raise self.THE_EXCEPTION


# ----------------------------------------------------------------------------
