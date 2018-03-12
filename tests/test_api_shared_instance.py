# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Shared Wiring instance API tests.
"""

from __future__ import absolute_import

import unittest

from . import mixin_test_api, mixin_use_shared_instance



class TestWiresAPI(mixin_test_api.TestWiresAPIMixin,
                   mixin_use_shared_instance.UseSharedInstanceMixin,
                   unittest.TestCase):

    """
    API tests for the shared Wiring instance.
    """


# ----------------------------------------------------------------------------
