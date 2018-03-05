# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------


from __future__ import absolute_import

import unittest

from . import mixin_test_singleton, mixin_test_args



class TestWiresNoArgPassing(mixin_test_singleton.TestWiresSingletonMixin,
                            mixin_test_args.TestWiresArgPassingMixin,
                            unittest.TestCase):

    expected_call_args = ()
    expected_call_kwargs = {}

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireArgPassing(mixin_test_singleton.TestWiresSingletonMixin,
                              mixin_test_args.TestWiresArgPassingMixin,
                              unittest.TestCase):

    wire1_args = (1, 2, 3)

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = {}

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireKwargPassing(mixin_test_singleton.TestWiresSingletonMixin,
                                mixin_test_args.TestWiresArgPassingMixin,
                                unittest.TestCase):

    wire1_kwargs = dict(a='a', b='b')

    expected_call_args = ()
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresWireArgKwargPassing(mixin_test_singleton.TestWiresSingletonMixin,
                                   mixin_test_args.TestWiresArgPassingMixin,
                                   unittest.TestCase):

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = {}



class TestWiresCallArgPassing(mixin_test_singleton.TestWiresSingletonMixin,
                              mixin_test_args.TestWiresArgPassingMixin,
                              unittest.TestCase):

    call_args = (1, 2, 3)

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = {}

    expected_2nd_call_args = (1, 2, 3)
    expected_2nd_call_kwargs = {}



class TestWiresCallKwargPassing(mixin_test_singleton.TestWiresSingletonMixin,
                                mixin_test_args.TestWiresArgPassingMixin,
                                unittest.TestCase):

    call_kwargs = dict(a='a', b='b')

    expected_call_args = ()
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = ()
    expected_2nd_call_kwargs = dict(a='a', b='b')



class TestWiresCallArgKwargPassing(mixin_test_singleton.TestWiresSingletonMixin,
                                   mixin_test_args.TestWiresArgPassingMixin,
                                   unittest.TestCase):

    call_args = (1, 2, 3)
    call_kwargs = dict(a='a', b='b')

    expected_call_args = (1, 2, 3)
    expected_call_kwargs = dict(a='a', b='b')

    expected_2nd_call_args = (1, 2, 3)
    expected_2nd_call_kwargs = dict(a='a', b='b')



class TestWiresFullPassing(mixin_test_singleton.TestWiresSingletonMixin,
                           mixin_test_args.TestWiresArgPassingMixin,
                           unittest.TestCase):

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    call_args = (4, 5, 6)
    call_kwargs = dict(c='c', d='d')

    expected_call_args = (1, 2, 3, 4, 5, 6)
    expected_call_kwargs = dict(a='a', b='b', c='c', d='d')

    expected_2nd_call_args = (4, 5, 6)
    expected_2nd_call_kwargs = dict(c='c', d='d')



class TestWiresDoubleFullPassing(mixin_test_singleton.TestWiresSingletonMixin,
                                 mixin_test_args.TestWiresArgPassingMixin,
                                 unittest.TestCase):

    wire1_args = (1, 2, 3)
    wire1_kwargs = dict(a='a', b='b')

    wire2_args = (4, 5, 6)
    wire2_kwargs = dict(c='c', d='d')

    call_args = (7, 8, 9)
    call_kwargs = dict(e='e', f='f')

    expected_call_args = (1, 2, 3, 7, 8, 9)
    expected_call_kwargs = dict(a='a', b='b', e='e', f='f')

    expected_2nd_call_args = (4, 5, 6, 7, 8, 9)
    expected_2nd_call_kwargs = dict(c='c', d='d', e='e', f='f')


# ----------------------------------------------------------------------------
