# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance caller/callee custom coupling tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_test_coupling



class TestCouplingReturnsTrue(mixin_test_coupling.WireAssertCouplingTestMixin,
                              unittest.TestCase):

    """
    Call time coupling tests for Wiring instances initialized with:
    - returns: True
    """


mixin_test_coupling.create_test_methods(
    TestCouplingReturnsTrue,
    {"returns": True},
)



class TestCouplingReturnsFalse(mixin_test_coupling.WireAssertCouplingTestMixin,
                               unittest.TestCase):

    """
    Call time coupling tests for Wiring instances initialized with:
    - returns: False
    """


mixin_test_coupling.create_test_methods(
    TestCouplingReturnsFalse,
    {"returns": False},
)


# ----------------------------------------------------------------------------
