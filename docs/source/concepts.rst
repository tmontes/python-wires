Concepts
========

This section describes the key concepts in Python Wires, pusposely omitting fine grained details. For that, refer to the :doc:`examples` and to the :doc:`reference`.



Wiring Objects
--------------

Python Wires provides a single public :class:`Wiring <wires._wiring.Wiring>` class. It encloses the available capabilities, exposing the full Python Wires API.

Using Python Wires revolves mostly around using :class:`Wiring <wires._wiring.Wiring>` object attributes. These are:

* Auto-created on first-access.
* Callable, like regular Python functions.

.. note::

    The :mod:`wires` package exports two names, :class:`Wiring <wires.Wiring>` and
    :attr:`w <wires.w>`: the first one is the :class:`Wiring <wires._wiring.Wiring>`
    class itself, while the second is a built-in, pre-initialized, shared,
    :class:`Wiring <wires._wiring.Wiring>` object, for quick usage.


:class:`Wiring <wires._wiring.Wiring>` objects and their callable attributes behave differently depending on initialization arguments. These can be overridden on a per-callable-attribute basis or even at call-time.


Wirings
-------

:class:`Wiring <wires._wiring.Wiring>` attributes (referred to as *wiring callables* from here on, given that they are callable) can be wired to one or more other callables.

Calling a *wiring callable* calls all its wired callables, in wiring order: this is the gist of Python Wires.

The *wiring callable*'s *wirings* is the list of its wired callables, in wiring order: a wire action adds a new callable to the end of this list, while an unwire one removes the first matching callable from it.

By default there are no limits on the minimum/maximum number of *wirings* a given *wiring callable* has. These can be enforced at the :class:`Wiring <wires._wiring.Wiring>` object's level, at initialization time (being applied to all *wiring callables* on that object), or at the *wiring callable*'s level, at any time, overriding its :class:`Wiring <wires._wiring.Wiring>` object's settings. With such limits in place:

* Wire actions fail when the current number of *wirings* is the maximum allowed.
* Unwire actions fail when the current number of *wirings* is the minimum allowed.
* Calling fails there are less than the minimum allowed number of *wirings*.

Additionally, changing *wiring callable*'s wiring limits fails when the current number of *wirings* is greater than zero and does not meet the new limits.



Argument Passing
----------------

*contents for section*



Call-time Coupling
------------------

*contents for section*

