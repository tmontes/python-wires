# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance caller/callee custom coupling tests.
"""


from __future__ import absolute_import

import sys
import unittest

from . import mixin_test_callables, mixin_test_coupling



def _test_class_name(wa):

    class_name_part = ''.join(
        '%s%s' % (str(k).capitalize(), str(v).capitalize())
        for k, v in wa.items()
    )
    return 'TestCoupling%s' % (class_name_part,)



def _generate_test_classes():

    call_coupling_arg_combinations = [
        {'returns': False},
        {'returns': True},
        {'ignore_failures': False},
        {'ignore_failures': True},
        {'returns': False, 'ignore_failures': False},
        {'returns': False, 'ignore_failures': True},
        {'returns': True, 'ignore_failures': False},
        {'returns': True, 'ignore_failures': True},
    ]

    base_classes = (
        mixin_test_callables.TestCallablesMixin,
        unittest.TestCase,
    )

    this_module = sys.modules[__name__]

    for wa in call_coupling_arg_combinations:
        test_class_name = _test_class_name(wa)
        test_class = type(test_class_name, base_classes, {})
        mixin_test_coupling.generate_tests(test_class, wa)
        setattr(this_module, test_class_name, test_class)


_generate_test_classes()


# ----------------------------------------------------------------------------
