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

    THE_EXCEPTION = ValueError('test exception value error message')
    raises_exception_callable = helpers.CallTracker(raises=THE_EXCEPTION)

    returns_42_callable = helpers.CallTracker(returns=42)
    returns_none_callable = helpers.CallTracker(returns=None)


# ----------------------------------------------------------------------------
