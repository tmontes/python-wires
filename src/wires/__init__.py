# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import



__version__ = '18.1.0b1'

__title__ = 'wires'
__description__ = 'Python Wires'

__license__ = 'MIT'
__uri__ = 'https://github.com/tmontes/python-wires/'

__author__ = 'Tiago Montes'
__email__ = 'tiago.montes@gmail.com'



from . _shell import WiresShell as Wires
from . _singleton import wire, unwire


# ----------------------------------------------------------------------------
