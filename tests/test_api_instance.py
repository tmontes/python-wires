# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance API tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_api, mixin_test_instance



class TestWiresAPI(mixin_test_api.TestWiresAPIMixin,
                   mixin_test_instance.TestWiresInstanceMixin,
                   unittest.TestCase):

    """
    API tests for Wires instances.
    """


# ----------------------------------------------------------------------------
