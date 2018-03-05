# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

from wires import wiring, wire, unwire



class TestWiresSingletonMixin(object):

    """
    Singleton Wires test mixin.
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
