# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Global Wires singleton API tests.
"""

from __future__ import absolute_import

import unittest

from . import mixin_test_api, mixin_test_singleton



class TestWiresAPI(mixin_test_singleton.TestWiresSingletonMixin,
                   mixin_test_api.TestWiresAPIMixin,
                   unittest.TestCase):

    """
    API tests for the global Wires singleton.
    """


# ----------------------------------------------------------------------------
