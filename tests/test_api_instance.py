# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_api, mixin_test_instance



class TestWiresAPI(mixin_test_api.TestWiresAPIMixin,
                   mixin_test_instance.TestWiresInstanceMixin,
                   unittest.TestCase):

    """
    Minimal API tests for the Wires singleton.
    """

    def setUp(self):

        self._w = Wiring()


# ----------------------------------------------------------------------------
