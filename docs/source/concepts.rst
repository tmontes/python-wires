Concepts
========

This section describes the key concepts in Python Wires, pusposely omitting fine grained details. For that, refer to the :doc:`examples` and to the :doc:`reference`.



Wires Objects
-------------

Python Wires provides a single, public :class:`Wires <wires._wires.Wires>` class, through which the full API is accessed. Using it revolves mostly around using :class:`Wires <wires._wires.Wires>` object attributes, which are:

* Auto-created on first-access.
* Callable, like regular Python functions.

Being callable, :class:`Wires <wires._wires.Wires>` object attributes will be referred to as **wires callables**, from here on.

:class:`Wires <wires._wires.Wires>` objects and their *wires callables* behave differently depending on initialization arguments. These can be overridden on a per-callable-attribute basis or even at call-time.


Wirings
-------

These principles describe the essence of Python Wires:

* *Wires callables* can be wired to one or more other callables.
* Calling a *wires callable* calls all its wired callables, in wiring order.

To support the remaining documentation, the following definitions are established:

wirings
    The list of *wires callable*'s wired callables, in wiring order.

number of wirings
    The length of *wirings*.

wire actions
    Add a new callable, which becomes wired, to the end of *wirings*.

unwire actions
    Remove the first matching wired callable from *wirings*.

By default there are no limits on the number of *wirings* a given *wires callable* has. Those can be enforced at the :class:`Wires <wires._wires.Wires>` object's level (set at initialization time and applicable to all *wires callables* on that object), or at the individual *wires callable*'s level (set at any time), overriding its :class:`Wires <wires._wires.Wires>` object's settings. With such limits in place:

* Wire actions fail when the current number of *wirings* is the maximum allowed.
* Unwire actions fail when the current number of *wirings* is the minimum allowed.
* Calling fails there are less than the minimum allowed number of *wirings*.

Additionally, changing *wires callable*'s wiring limits fails when the current number of *wirings* is greater than zero and does not meet the new limits.



Argument Passing
----------------

*contents for section*



Call-time Coupling
------------------

*contents for section*

