# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Call Wires.
"""

from __future__ import absolute_import

from . import _instance



class WiresShell(object):

    def __init__(self):

        self._wires_instance = _instance.WiresInstance()


    @property
    def wire(self):

        self._wires_instance.wire_context = True
        return self._wires_instance


    @property
    def unwire(self):

        self._wires_instance.wire_context = False
        return self._wires_instance


    def __getattr__(self, name):

        return getattr(self._wires_instance, name)


# ----------------------------------------------------------------------------
