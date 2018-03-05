# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance test mixin.
"""


from __future__ import absolute_import

from wires import Wiring



class TestWiresInstanceMixin(object):

    """
    Wires instance test mixin.
    """

    def setUp(self):
        """
        Need a per-test instance: classes we mixin with must call this.
        """
        self._w = Wiring()


    @property
    def w(self):
        """
        Per test mixin contract: self.w is a Wiring instance.
        """
        return self._w


    @property
    def wire(self):
        """
        Per test mixin contract: self.wire wires callables.
        """
        return self._w.wire


    @property
    def unwire(self):
        """
        Per test mixin contract: self.unwire unwires callabless.
        """
        return self._w.unwire


# ----------------------------------------------------------------------------
