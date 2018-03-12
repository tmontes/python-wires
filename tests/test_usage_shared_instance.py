# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Shared Wiring instance generic usage tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_usage, mixin_use_shared_instance



class TestWiresUtilization(mixin_use_shared_instance.UseSharedInstanceMixin,
                           mixin_test_usage.TestWiresUsageMixin,
                           unittest.TestCase):

    """
    Utilization tests for the shared Wiring instance.
    """


# ----------------------------------------------------------------------------
