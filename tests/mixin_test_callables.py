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

    EXCEPTION = ValueError('test exception value error message')
    raises_exception = helpers.CallTracker(raises=EXCEPTION)

    returns_42 = helpers.CallTracker(returns=42)
    returns_none = helpers.CallTracker(returns=None)


# ----------------------------------------------------------------------------
