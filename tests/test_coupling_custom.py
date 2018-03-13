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



class TestCouplingTrue(mixin_test_coupling.WireAssertCouplingTestMixin,
                       unittest.TestCase):

    """
    Call time coupling tests for Wiring instances initialized with:
    - coupling: True
    """


mixin_test_coupling.create_test_methods(TestCouplingTrue, {"coupling": True})



class TestCouplingFalse(mixin_test_coupling.WireAssertCouplingTestMixin,
                        unittest.TestCase):

    """
    Call time coupling tests for Wiring instances initialized with:
    - coupling: False
    """


mixin_test_coupling.create_test_methods(TestCouplingFalse, {"coupling": False})


# ----------------------------------------------------------------------------
