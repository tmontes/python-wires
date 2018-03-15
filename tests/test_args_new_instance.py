# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Wires instance argument passing tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_use_new_instance, mixin_test_args



class TestWiresNoArgPassing(mixin_use_new_instance.UseNewInstanceMixin,
                            mixin_test_args.TestWiresNoArgPassingMixin,
                            unittest.TestCase):

    """
    Wires instance no argument call tests.
    """



class TestWiresWireArgPassing(mixin_use_new_instance.UseNewInstanceMixin,
                              mixin_test_args.TestWiresWireArgPassingMixin,
                              unittest.TestCase):

    """
    Wires instance wire-time positional argument passing call tests.
    """



class TestWiresWireKwargPassing(mixin_use_new_instance.UseNewInstanceMixin,
                                mixin_test_args.TestWiresWireKwargPassingMixin,
                                unittest.TestCase):

    """
    Wires instance wire-time named argument passing call tests.
    """



class TestWiresWireArgKwargPassing(mixin_use_new_instance.UseNewInstanceMixin,
                                   mixin_test_args.TestWiresWireArgKwargPassingMixin,
                                   unittest.TestCase):

    """
    Wires instance wire-time positional and named argument passing call tests.
    """



class TestWiresCallArgPassing(mixin_use_new_instance.UseNewInstanceMixin,
                              mixin_test_args.TestWiresCallArgPassingMixin,
                              unittest.TestCase):

    """
    Wires instance call-time positional argument passing call tests.
    """



class TestWiresCallKwargPassing(mixin_use_new_instance.UseNewInstanceMixin,
                                mixin_test_args.TestWiresCallKwargPassingMixin,
                                unittest.TestCase):

    """
    Wires instance call-time named argument passing call tests.
    """



class TestWiresCallArgKwargPassing(mixin_use_new_instance.UseNewInstanceMixin,
                                   mixin_test_args.TestWiresCallArgKwargPassingMixin,
                                   unittest.TestCase):

    """
    Wires instance call-time positional and named argument passing call tests.
    """



class TestWiresFullPassing(mixin_use_new_instance.UseNewInstanceMixin,
                           mixin_test_args.TestWiresFullPassingMixin,
                           unittest.TestCase):

    """
    Wires instance wire-time and call-time positional and named argument passing
    call tests.
    """



class TestWiresDoubleFullPassing(mixin_use_new_instance.UseNewInstanceMixin,
                                 mixin_test_args.TestWiresDoubleFullPassingMixin,
                                 unittest.TestCase):

    """
    Wires instance double wiring wire-time and call-time positional and named
    argument passing call tests.
    """


# ----------------------------------------------------------------------------
