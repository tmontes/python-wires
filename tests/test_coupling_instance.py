# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance caller/callee coupling tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_instance, mixin_test_coupling



class TestWiresCoupling(mixin_test_instance.TestWiresInstanceMixin,
                        mixin_test_coupling.TestCallerCalleeCouplingMixin,
                        unittest.TestCase):

    """
    Caller/callee tests for Wires instances.
    """


# ----------------------------------------------------------------------------
