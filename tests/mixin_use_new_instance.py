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



class UseNewInstanceMixin(object):

    """
    Wires tests with new instances mixin.
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


# ----------------------------------------------------------------------------
