# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_usage, mixin_test_instance



class TestWiresUtilization(mixin_test_instance.TestWiresInstanceMixin,
                           mixin_test_usage.TestWiresUsageMixin,
                           unittest.TestCase):

    """
    Utilization tests for the Wires instances.
    """

    def setUp(self):

        self._w = Wiring()


# ----------------------------------------------------------------------------
