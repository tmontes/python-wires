# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Shared Wires instance test mixin.
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
        Per test mixin contract: self.w is a Wires instance.
        """
        return w


    @staticmethod
    def tearDown():
        """
        Ensures the shared instance has no pending callables.
        """
        existing_callables = set(w)
        for existing_callable in existing_callables:
            delattr(w, existing_callable.__name__)


# ----------------------------------------------------------------------------
