# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Wires Singleton.
"""

from __future__ import absolute_import

from . import _shell



_WIRING_SINGLETON = _shell.WiringShell()

wiring = _WIRING_SINGLETON
wire = _WIRING_SINGLETON.wire
unwire = _WIRING_SINGLETON.unwire


# ----------------------------------------------------------------------------
