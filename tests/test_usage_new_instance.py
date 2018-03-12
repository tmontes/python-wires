# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance generic usage tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_usage, mixin_use_new_instance



class TestWiresUtilization(mixin_use_new_instance.UseNewInstanceMixin,
                           mixin_test_usage.TestWiresUsageMixin,
                           unittest.TestCase):

    """
    Utilization tests for the Wires instances.
    """


# ----------------------------------------------------------------------------
