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

    pass



class TestWiresWireArgPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                              mixin_test_args.TestWiresWireArgPassingMixin,
                              unittest.TestCase):

    pass



class TestWiresWireKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                mixin_test_args.TestWiresWireKwargPassingMixin,
                                unittest.TestCase):

    pass



class TestWiresWireArgKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                   mixin_test_args.TestWiresWireArgKwargPassingMixin,
                                   unittest.TestCase):

    pass



class TestWiresCallArgPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                              mixin_test_args.TestWiresCallArgPassingMixin,
                              unittest.TestCase):

    pass



class TestWiresCallKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                mixin_test_args.TestWiresCallKwargPassingMixin,
                                unittest.TestCase):

    pass



class TestWiresCallArgKwargPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                   mixin_test_args.TestWiresCallArgKwargPassingMixin,
                                   unittest.TestCase):

    pass



class TestWiresFullPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                           mixin_test_args.TestWiresFullPassingMixin,
                           unittest.TestCase):

    pass



class TestWiresDoubleFullPassing(mixin_use_shared_instance.UseSharedInstanceMixin,
                                 mixin_test_args.TestWiresDoubleFullPassingMixin,
                                 unittest.TestCase):

    pass


# ----------------------------------------------------------------------------
