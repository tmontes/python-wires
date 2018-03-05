# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Global Wires singleton caller/callee tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_singleton, mixin_test_coupling



class TestWiresCoupling(mixin_test_singleton.TestWiresSingletonMixin,
                        mixin_test_coupling.TestCallerCalleeCouplingMixin,
                        unittest.TestCase):

    """
    Caller/callee tests for the Wires singleton.
    """


# ----------------------------------------------------------------------------
