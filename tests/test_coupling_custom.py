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



# About these tests
# -----------------
# This module dynamically generates test classes for all possible instantiation
# time call coupling parameter combinations.
#
# Refer to the documentation in `mixin_test_coupling` for more details.



def _test_class_name(wa):

    # Test class names include instantiation-time argument names and values.

    class_name_part = ''.join(
        '%s%s' % (str(k).capitalize(), str(v).capitalize())
        for k, v in wa.items()
    )
    return 'TestCoupling%s' % (class_name_part,)



def _generate_test_classes():

    # Generates one test class for each combination of possible instantiation
    # time call coupling argument parameters; the empty argument dict is
    # excluded given that it is already accounted for in the explicitly created
    # `TestCouplingMixin` in `mixin_test_coupling`.
    #
    # Uses `mixin_test_coupling.generate_tests` to populate the class with
    # test case sets.

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


# Generate the actual test classes.

_generate_test_classes()


# ----------------------------------------------------------------------------
