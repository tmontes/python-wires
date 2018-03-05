# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import



class TestWiresInstanceMixin(object):

    """
    Wires instance test mixin, requiring mixed classes to have:
    - self._w as a Wiring instance.
    """

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
