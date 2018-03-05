# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from wires import wiring, wire, unwire

from . import mixin_test_api



class TestWiresAPI(mixin_test_api.TestWiresAPIMixin, unittest.TestCase):

    """
    Minimal API tests for the Wires singleton.
    """

    @property
    def w(self):

        return wiring


    @property
    def wire(self):

        return wire


    @property
    def unwire(self):

        return unwire


# ----------------------------------------------------------------------------
