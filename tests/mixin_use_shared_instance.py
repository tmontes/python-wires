# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Shared Wiring instance test mixin.
"""


from __future__ import absolute_import

from wires import w



class UseSharedInstanceMixin(object):

    """
    Wires tests with shared instance mixin.
    """

    @property
    def w(self):
        """
        Per test mixin contract: self.w is a Wiring instance.
        """
        return w


# ----------------------------------------------------------------------------
