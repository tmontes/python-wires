# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance min/max callee tests.
"""


from __future__ import absolute_import

import unittest

from wires import Wiring

from . import mixin_test_callees



class TestMinMaxCallee(mixin_test_callees.TestCalleesMixin, unittest.TestCase):

    """
    min/max callee tests for Wires instances.
    """

    def test_min_none_max_none_wire_unwire(self):
        """
        Wiring a single callable works.
        """
        w = Wiring(min_callees=None, max_callees=None)

        w.wire.this.calls_to(self.returns_42_callee)
        w.unwire.this.calls_to(self.returns_42_callee)


# ----------------------------------------------------------------------------
