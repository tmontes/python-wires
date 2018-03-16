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

from . import mixin_use_new_instance, mixin_test_coupling



class TestWiresCoupling(mixin_use_new_instance.UseNewInstanceMixin,
                        mixin_test_coupling.TestCouplingMixin,
                        unittest.TestCase):

    """
    Call-time coupling tests for Wiring instances.
    """


# ----------------------------------------------------------------------------
