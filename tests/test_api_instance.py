# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_api



class TestWiresAPI(mixin_test_api.TestWiresAPIMixin, unittest.TestCase):

    """
    Minimal API tests for the Wires singleton.
    """

    def setUp(self):

        self._w = Wiring()


    @property
    def w(self):

        return self._w


    @property
    def wire(self):

        return self._w.wire


    @property
    def unwire(self):

        return self._w.unwire


# ----------------------------------------------------------------------------
