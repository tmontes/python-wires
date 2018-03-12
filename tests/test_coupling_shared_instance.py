# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Shared Wiring instance caller/callee tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_use_shared_instance, mixin_test_coupling



class TestWiresCoupling(mixin_use_shared_instance.UseSharedInstanceMixin,
                        mixin_test_coupling.TestCallerCalleeCouplingMixin,
                        unittest.TestCase):

    """
    Caller/callee tests for the shared Wiring instance.
    """


# ----------------------------------------------------------------------------
