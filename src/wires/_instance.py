# ----------------------------------------------------------------------------
# Python Wires Tests
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for deatils.
# ----------------------------------------------------------------------------

"""
Python Call Wires.
"""

from __future__ import absolute_import

from . import _callable



class WiresInstance(object):

    """
    Callable based event manager with a minimal API.
    Summary:
    - Events are attributes of Wires, created dynamically, as needed.
    - Events have zero or more handlers: functions/callables added to them.
    - Events are fired by calling them, like functions.
    - Firing an event calls all associated handlers, passing them the same
      arguments the "fire event" call was given.

    Usage example:

    >>> em = Wires()

    # Tell the event manager to call our lambda when 'my_event' is fired.
    >>> em.my_event.calls(lambda: print('event handler #1'))

    # Adding another callable for 'my_event':
    >>> em.my_event.calls(lambda: print('event handler #2'))

    # Trigger 'my_event'
    >>> em.my_event()
    event handler #1
    event handler #2
    """

    def __init__(self):

        # Tracks known Callable instances:
        # - Keys are callable names (my dynamic attributes).
        # - Values are Callable objects.

        self._callables = {}

        # TODO: explain this
        self.wire_context = True


    def __getattr__(self, name):

        # Called on attribute access, returns an event object.
        # Either uses an tracked one or creates new one, tracking it.

        try:
            return self._callables[name]
        except KeyError:
            new_callable = _callable.Callable(name, self)
            self._callables[name] = new_callable
            return new_callable


# ----------------------------------------------------------------------------
