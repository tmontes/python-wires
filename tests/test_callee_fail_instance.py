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

        mixin_test_instance.TestWiresInstanceMixin.setUp(self)
        mixin_test_callee_fail.TestWiresCalleeFailMixin.setUp(self)


    def tearDown(self):

        mixin_test_callee_fail.TestWiresCalleeFailMixin.tearDown(self)


# ----------------------------------------------------------------------------
