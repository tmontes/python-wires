API Usage Examples
==================


.. note::

    Under Python 2.7, some of these examples require the following import statement
    at the top:

    .. code-block:: python

        from __future__ import print_function




Getting a Wires object
----------------------

Python Wires ships with a built-in, shared, readily usable :class:`Wires <wires._wires.Wires>` object, called :attr:`w <wires.w>`.

.. code-block:: python

    from wires import w             # `w` is a built-in, shared `Wires` object


Alternatively, :class:`Wires <wires._wires.Wires>` objects are created with:


.. code-block:: python

    from wires import Wires

    w = Wires()


The :class:`Wires <wires._wires.Wires>` class :meth:`initializer <wires._wires.Wires.__init__>` supports optional arguments to override the default behaviour. For example, here's a :class:`Wires <wires._wires.Wires>` object requiring its *wires callables* to have exactly one wiring:

.. code-block:: python

    from wires import Wires

    w = Wires(min_wirings=1, max_wirings=1)




Wiring and Unwiring
-------------------

The :meth:`wire <wires._callable.WiresCallable.wire>` method wires a callable to a *wires callable* [#wirescallable]_:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.one_callable.wire(say_hi)         # calling `w.one_callable` will call `say_hi`


Multiple wirings to the same callable are allowed:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.one_callable.wire(say_hi)         # calling `w.one_callable` will call `say_hi`
    w.one_callable.wire(say_hi)         # calling `w.one_callable` will call `say_hi` twice




Wiring a non-callable raises a :class:`TypeError` exception:

.. code-block:: python

    from wires import w

    w.one_callable.wire(42)             # raises TypeError: 42 isn't callable


The :meth:`unwire <wires._callable.WiresCallable.unwire>` method unwires a given callable:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.one_callable.wire(say_hi)         # calling `w.one_callable` will call `say_hi`
    w.one_callable.unwire(say_hi)       # calling `w.one_callable` no longer calls `say_hi`



If multiple wirings exist, :meth:`unwire <wires._callable.WiresCallable.unwire>` unwires the first matching wiring only:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.one_callable.wire(say_hi)         # calling `w.one_callable` will call `say_hi`
    w.one_callable.wire(say_hi)         # calling `w.one_callable` will call `say_hi` twice
    w.one_callable.unwire(say_hi)       # calling `w.one_callable` will call `say_hi` once
    w.one_callable.unwire(say_hi)       # calling `w.one_callable` no longer calls `say_hi`



Unwiring a non-wired callable raises a :class:`ValueError`

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.one_callable.unwire(say_hi)       # raises ValueError: non-wired `say_hi`




Wiring Limits
-------------

Limiting the number of wirings on *wires callables* can be done in two different ways.

Using a custom-initialized :class:`Wires <wires._wires.Wires>` object, its *wires callables* default to its wiring limits:

.. code-block:: python

    from wires import Wires

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w = Wires(min_wirings=1, max_wirings=1)

    w.one_callable.wire(say_hi)
    w.one_callable.wire(say_bye)        # raises RuntimeError: max_wirings limit reached
    w.one_callable.unwire(say_hi)       # raises RuntimeError: min_wirings limit reached


Overriding wiring limits on a per-*wires callable* basis:

.. code-block:: python

    from wires import Wires

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w = Wires()                         # defaults to no wiring limits

    w.one_callable.min_wirings = 1      # set `w.one_callable`'s min wirings
    w.one_callable.max_wirings = 1      # set `w.one_callable`'s max wirings

    w.one_callable.wire(say_hi)
    w.one_callable.wire(say_bye)        # raises RuntimeError: max_wirings limit reached
    w.one_callable.unwire(say_hi)       # raises RuntimeError: min_wirings limit reached

    w.another_callable.wire(say_hi)
    w.another_callable.wire(say_bye)    # works, no limits on `w.another_callable`
    w.another_callable.unwire(say_bye)  # works, no limits on `w.another_callable`
    w.another_callable.unwire(say_hi)   # works, no limits on `w.another_callable`


Clearing wiring limits on a per-*wires callable* basis:

.. code-block:: python

    from wires import Wires

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w = Wires(min_wirings=1, max_wirings=1)

    w.one_callable.min_wirings = None   # no min wiring limit on `w.one_callable`
    w.one_callable.max_wirings = None   # no max wiring limit on `w.one_callable`

    w.one_callable.wire(say_hi)
    w.one_callable.wire(say_bye)        # works, no limits on `w.one_callable`
    w.one_callable.unwire(say_bye)      # works, no limits on `w.one_callable`
    w.one_callable.unwire(say_hi)       # works, no limits on `w.one_callable`

    w.another_callable.wire(say_hi)
    w.another_callable.wire(say_bye)    # raises RuntimeError: max_wirings limit reached
    w.another_callable.unwire(say_hi)   # raises RuntimeError: min_wirings limit reached


Overriding per-*wires callable* wiring limits raises a :class:`ValueError` when:

    * There is at least one wiring.
    * The current wirings don't meet the limit trying to be set.

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.one_callable.wire(say_hi)
    w.one_callable.min_wirings = 2      # raises ValueError: too few wirings



Calling
-------

Calling a just-created, default *wires callable* works:

.. code-block:: python

    from wires import w

    w.one_callable()


Calling a *wires callable* calls its wired callables, in wiring order:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w.one_callable.wire(say_hi)
    w.one_callable.wire(say_bye)
    w.one_callable()                    # calls `say_hi` first, then `say_bye`

    w.another_callable.wire(say_bye)
    w.another_callable.wire(say_hi)
    w.another_callable()                # calls `say_bye` first, then `say_hi`


Calling a *wires callable* where the current number of wirings is below the minimum wiring limit raises a :class:`ValueError` (set by the :class:`Wires <wires._wires.Wires>` object or overriden at the *wires callable* level):

.. code-block:: python

    from wires import w

    w.one_callable.min_wirings = 1
    w.one_callable()                    # raises ValueError: less than min_wirings wired



Argument Passing
----------------

Call-time arguments are passed to each wired callable:

.. code-block:: python

    from wires import w

    def a_print(*args, **kw):
        print('args=%r kw=%r' % (args, kw))

    w.one_callable.wire(a_print)
    w.one_callable()                    # prints: args=() kw={}
    w.one_callable(42, 24)              # prints: args=(42, 24) kw={}
    w.one_callable(a=42, b=24)          # prints: args=() kw={'a': 42, 'b': 24}
    w.one_callable(42, a=24)            # prints: args=(42,) kw={'a': 24}


Wiring actions can include wire-time arguments, later combined with call-time arguments:

.. code-block:: python

    from wires import w

    def a_print(*args, **kw):
        print('args=%r kw=%r' % (args, kw))

    w.one_callable.wire(a_print, 'one')
    w.another_callable.wire(a_print, a='nother')

    w.one_callable()                    # prints: args=('one',) kw={}
    w.one_callable(42, 24)              # prints: args=('one', 42, 24) kw={}
    w.one_callable(a=42, b=24)          # prints: args=('one',) kw={'a': 42, 'b': 24}
    w.one_callable(42, a=24)            # prints: args=('one', 42) kw={'a': 24}

    w.another_callable()                # prints: args=() kw={'a': 'nother'}
    w.another_callable(42, 24)          # prints: args=(42, 24) kw={'a': 'nother'}
    w.another_callable(a=42, b=24)      # prints: args=() kw={'a': 42, 'b': 24}
    w.another_callable(42, a=24)        # prints: args=(42,) kw={'a': 24}




Call-time coupling
------------------




Introspection
-------------



.. [#wirescallable] Per the :doc:`concepts` section, *wires callables* are :class:`Wires <wires._wires.Wires>` object auto-created attributes.
