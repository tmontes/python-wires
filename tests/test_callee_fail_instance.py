# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_instance, mixin_test_callee_fail



class TestWiresCalleeFail(mixin_test_instance.TestWiresInstanceMixin,
                          mixin_test_callee_fail.TestWiresCalleeFailMixin,
                          unittest.TestCase):

    """
    Callee failure tests using the Wires singleton.
    """

    def setUp(self):

        self._w = Wiring()
        mixin_test_callee_fail.TestWiresCalleeFailMixin.mixin_setUp(self)


    def tearDown(self):

        mixin_test_callee_fail.TestWiresCalleeFailMixin.mixin_tearDown(self)


# ----------------------------------------------------------------------------
