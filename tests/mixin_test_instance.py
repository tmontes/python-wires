# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

from wires import Wiring



class TestWiresInstanceMixin(object):

    """
    Wires instance test mixin.
    """

    def setUp(self):

        self._w = Wiring()


    @property
    def w(self):

        return self._w


    @property
    def wire(self):

        return self._w.wire


    @property
    def unwire(self):

        return self._w.unwire


# ----------------------------------------------------------------------------
