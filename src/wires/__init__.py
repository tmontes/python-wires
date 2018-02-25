# ----------------------------------------------------------------------------
# Python Wires
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import



__version__ = '0.1.0a1'

__title__ = 'wires'
__description__ = 'Python Wires'

__license__ = 'MIT'
__uri__ = 'https://github.com/tmontes/wires/'

__author__ = 'Tiago Montes'
__email__ = ''



from . _shell import WiresShell as Wires
from . _singleton import wire, unwire


# ----------------------------------------------------------------------------
