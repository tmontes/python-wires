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



class TestMinMaxCallee(unittest.TestCase):

    """
    min/max callee tests for Wires instances.
    """

    def test_min_none_max_none_wire(self):
        """
        Wiring a single callable works.
        """
        w = Wiring(min_callees=None, max_callees=None)

        # TODO: keep working on this
        w.wire.this.calls_to(print)


# ----------------------------------------------------------------------------
