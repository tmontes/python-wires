# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Shared Wiring instance argument passing tests.
"""


from __future__ import absolute_import

import unittest

from . import mixin_use_shared_instance, mixin_test_args



class TestWiresNoArgPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                            mixin_test_args.TestWiresNoArgPassingMixin,
                            unittest.TestCase):

    """
    Shared Wires instance no argument call tests.
    """



class TestWiresWireArgPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                              mixin_test_args.TestWiresWireArgPassingMixin,
                              unittest.TestCase):

    """
    Shared Wires instance wire-time positional argument passing call tests.
    """



class TestWiresWireKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                mixin_test_args.TestWiresWireKwargPassingMixin,
                                unittest.TestCase):

    """
    Shared Wires instance wire-time named argument passing call tests.
    """



class TestWiresWireArgKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                   mixin_test_args.TestWiresWireArgKwargPassingMixin,
                                   unittest.TestCase):

    """
    Shared Wires instance wire-time positional and named argument passing call
    tests.
    """



class TestWiresCallArgPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                              mixin_test_args.TestWiresCallArgPassingMixin,
                              unittest.TestCase):

    """
    Shared Wires instance call-time positional argument passing call tests.
    """



class TestWiresCallKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                mixin_test_args.TestWiresCallKwargPassingMixin,
                                unittest.TestCase):

    """
    Shared Wires instance call-time named argument passing call tests.
    """



class TestWiresCallArgKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                   mixin_test_args.TestWiresCallArgKwargPassingMixin,
                                   unittest.TestCase):

    """
    Shared Wires instance call-time positional and named argument passing call
    tests.
    """



class TestWiresFullPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                           mixin_test_args.TestWiresFullPassingMixin,
                           unittest.TestCase):

    """
    Shared Wires instance wire-time and call-time positional and named argument
    passing call tests.
    """



class TestWiresDoubleFullPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                 mixin_test_args.TestWiresDoubleFullPassingMixin,
                                 unittest.TestCase):

    """
    Shared Wires instance double wiring wire-time and call-time positional and
    named argument passing call tests.
    """


# ----------------------------------------------------------------------------
