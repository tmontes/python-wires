# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Global Wires singleton generic usage tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_usage, mixin_test_singleton



class TestWiresUtilization(mixin_test_singleton.TestWiresSingletonMixin,
                           mixin_test_usage.TestWiresUsageMixin,
                           unittest.TestCase):

    """
    Utilization tests for the Wires singleton.
    """


# ----------------------------------------------------------------------------
