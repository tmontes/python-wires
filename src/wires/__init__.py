# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Python Wires
"""

from __future__ import absolute_import



__version__ = '19.2.0'

__title__ = 'wires'
__description__ = 'Python Wires'

__license__ = 'MIT'
__uri__ = 'https://github.com/tmontes/python-wires/'

__author__ = 'Tiago Montes'
__email__ = 'tiago.montes@gmail.com'


from . _wires import Wires
from . _shared import w


__all__ = ['Wires', 'w']


# ----------------------------------------------------------------------------
