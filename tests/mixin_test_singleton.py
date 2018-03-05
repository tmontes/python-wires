# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Global Wires singleton test mixin.
"""


from __future__ import absolute_import

from wires import wiring, wire, unwire



class TestWiresSingletonMixin(object):

    """
    Singleton Wires test mixin.
    """

    @property
    def w(self):
        """
        Per test mixin contract: self.w is a Wiring instance.
        """
        return wiring


    @property
    def wire(self):
        """
        Per test mixin contract: self.wire wires callables.
        """
        return wire


    @property
    def unwire(self):
        """
        Per test mixin contract: self.unwire unwires callabless.
        """
        return unwire


# ----------------------------------------------------------------------------
