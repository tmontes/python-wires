Concepts
========

This section describes the key concepts in Python Wires, purposely omitting sample code and fine grained details. For that, refer to the :doc:`examples` and to the :doc:`reference`.



Wires Objects
-------------

Python Wires provides a single, public :class:`Wires <wires._wires.Wires>` class, through which the full API is accessed. Using it revolves mostly around using :class:`Wires <wires._wires.Wires>` object attributes, which are:

* Auto-created on first-access.
* Callable, like regular Python functions.

Being callable, :class:`Wires <wires._wires.Wires>` object attributes will be referred to as **wires callables**, from here on.

:class:`Wires <wires._wires.Wires>` objects and their *wires callables* behave differently depending on initialization arguments. These can be overridden on a per-*wires callable* basis or even at call-time.



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

By default there are no limits on the *number of wirings* a given *wires callable* has. Those can be enforced at the :class:`Wires <wires._wires.Wires>` object's level (set at initialization time and applicable to all *wires callables* on that object), or at the individual *wires callable*'s level (set at any time), overriding its :class:`Wires <wires._wires.Wires>` object's settings. With such limits in place:

* Wire actions fail when the current *number of wirings* is the maximum allowed.
* Unwire actions fail when the current *number of wirings* is the minimum allowed.
* Calling fails there are less than the minimum allowed *number of wirings*.

Additionally, changing *wires callable*'s wiring limits fails when the current *number of wirings* is greater than zero and does not meet the new limits.



Argument Passing
----------------

Like regular Python functions, *wires callables* can be passed positional and keyword arguments at call-time. Additionally, wire-time positional and keyword arguments can be set on each *wire action*.

At call-time, each wired callable is passed a combination of its wire-time arguments with the call-time arguments:

* Call-time positional arguments are passed by position, after wire-time positional arguments.
* Call-time keyword arguments are passed by name, overriding wire-time keyword arguments named alike.

Handling arguments is up to each individual wired callable. The way failures are handled, including argument mismatching ones is described next.


.. _concepts-calltime-coupling:

Call-time Coupling
------------------

Call-time coupling defines how coupled/decoupled are the callers of *wires callables* from the respective wired callables.

By default, call-time coupling is fully decoupled:

* Calling a *wires callable* returns ``None``, regardless of what each wired callable
  returns or whether or not calling a given wired callable raises an exception.

* All wired callables will be called, in order, regardless of the fact that calling a
  given wired callable may raise an exception.


Call-time coupling behaviour can be changed with two independent flags:

* **Ignore Exceptions**

    * When *on*, all wired callables are called, in order, regardless
      of the fact that calling a given wired callable may raise an exception.

    * When *off*, no further wired callables will be called once calling a given
      wired callable raises an exception.

* **Returns**

    * When *off*, calling a *wires callable* always returns ``None``.
    * When *on*, calling a *wires callable* will return a value or raise an
      exception:

        * An exception will be raised when **Ignore Exceptions** is *off* and
          calling a wired callable raises an exception.

        * A value is returned in every other case: a list of ``(<exception>, <result>)``
          tuples containing either the raised ``<exception>`` or returned ``<result>``
          for each wired callable, in the wiring order.


Call-time coupling flags can be set at :class:`Wires <wires._wires.Wires>` objects initialization time (applicable to all *wires callables* on that object), defined on a per-*wires callable* basis, or overridden at call-time.

