# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Wires instance test mixin.
"""


from __future__ import absolute_import

from wires import Wires



class UseNewInstanceMixin(object):

    """
    Wires tests with new instances mixin.
    """

    def setUp(self):
        """
        Need a per-test instance: classes we mixin with must call this.
        """
        self._w = Wires()


    @property
    def w(self):
        """
        Per test mixin contract: self.w is a Wires instance.
        """
        return self._w


# ----------------------------------------------------------------------------
