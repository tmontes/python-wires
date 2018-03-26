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

    w.callable.wire(say_hi)             # calling `w.callable` will call `say_hi`


Multiple wirings to the same callable are allowed:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.callable.wire(say_hi)             # calling `w.callable` will call `say_hi`
    w.callable.wire(say_hi)             # calling `w.callable` will call `say_hi` twice




Wiring a non-callable raises a :class:`TypeError` exception:

.. code-block:: python

    from wires import w

    w.callable.wire(42)                 # raises TypeError: 42 isn't callable


The :meth:`unwire <wires._callable.WiresCallable.unwire>` method unwires a given callable:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.callable.wire(say_hi)             # calling `w.callable` will call `say_hi`
    w.callable.unwire(say_hi)           # calling `w.callable` no longer calls `say_hi`



If multiple wirings exist, :meth:`unwire <wires._callable.WiresCallable.unwire>` unwires the first matching wiring only:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.callable.wire(say_hi)             # calling `w.callable` will call `say_hi`
    w.callable.wire(say_hi)             # calling `w.callable` will call `say_hi` twice
    w.callable.unwire(say_hi)           # calling `w.callable` will call `say_hi` once
    w.callable.unwire(say_hi)           # calling `w.callable` no longer calls `say_hi`



Unwiring a non-wired callable raises a :class:`ValueError`:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.callable.unwire(say_hi)           # raises ValueError: non-wired `say_hi`




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

    w.callable.wire(say_hi)
    w.callable.wire(say_bye)            # raises RuntimeError: max_wirings limit reached
    w.callable.unwire(say_hi)           # raises RuntimeError: min_wirings limit reached


Overriding wiring limits on a *wires callable* basis:

.. code-block:: python

    from wires import Wires

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w = Wires()                         # defaults to no wiring limits

    w.callable1.min_wirings = 1         # set `w.callable1`'s min wirings
    w.callable1.max_wirings = 1         # set `w.callable1`'s max wirings

    w.callable1.wire(say_hi)
    w.callable1.wire(say_bye)           # raises RuntimeError: max_wirings limit reached
    w.callable1.unwire(say_hi)          # raises RuntimeError: min_wirings limit reached

    w.callable2.wire(say_hi)
    w.callable2.wire(say_bye)           # works, no limits on `w.callable2`
    w.callable2.unwire(say_bye)         # works, no limits on `w.callable2`
    w.callable2.unwire(say_hi)          # works, no limits on `w.callable2`


Clearing wiring limits on a per-*wires callable* basis:

.. code-block:: python

    from wires import Wires

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w = Wires(min_wirings=1, max_wirings=1)

    w.callable1.min_wirings = None      # no min wiring limit on `w.callable1`
    w.callable1.max_wirings = None      # no max wiring limit on `w.callable1`

    w.callable1.wire(say_hi)
    w.callable1.wire(say_bye)           # works, no limits on `w.callable1`
    w.callable1.unwire(say_bye)         # works, no limits on `w.callable1`
    w.callable1.unwire(say_hi)          # works, no limits on `w.callable1`

    w.callable2.wire(say_hi)
    w.callable2.wire(say_bye)           # raises RuntimeError: max_wirings limit reached
    w.callable2.unwire(say_hi)          # raises RuntimeError: min_wirings limit reached


Overriding per-*wires callable* wiring limits raises a :class:`ValueError` when:

    * There is at least one wiring.
    * The current wirings don't meet the limit trying to be set.

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    w.callable.wire(say_hi)
    w.callable.min_wirings = 2          # raises ValueError: too few wirings



Calling
-------

Calling a just-created, default *wires callable* works:

.. code-block:: python

    from wires import w

    w.callable()


Calling a *wires callable* calls its wired callables, in wiring order:

.. code-block:: python

    from wires import w

    def say_hi():
        print('Hello from wires!')

    def say_bye():
        print('Bye, see you soon.')

    w.callable1.wire(say_hi)
    w.callable1.wire(say_bye)
    w.callable1()                       # calls `say_hi` first, then `say_bye`

    w.callable2.wire(say_bye)
    w.callable2.wire(say_hi)
    w.callable2()                       # calls `say_bye` first, then `say_hi`


Calling a *wires callable* where the current number of wirings is below the minimum wiring limit raises a :class:`ValueError` (set by the :class:`Wires <wires._wires.Wires>` object or overriden at the *wires callable* level):

.. code-block:: python

    from wires import w

    w.callable.min_wirings = 1
    w.callable()                        # raises ValueError: less than min_wirings wired



Argument Passing
----------------

Call-time arguments are passed to each wired callable:

.. code-block:: python

    from wires import w

    def a_print(*args, **kw):
        print('args=%r kw=%r' % (args, kw))

    w.callable.wire(a_print)
    w.callable()                        # prints: args=() kw={}
    w.callable(42, 24)                  # prints: args=(42, 24) kw={}
    w.callable(a=42, b=24)              # prints: args=() kw={'a': 42, 'b': 24}
    w.callable(42, a=24)                # prints: args=(42,) kw={'a': 24}


Wiring actions can include wire-time arguments, later combined with call-time arguments:

.. code-block:: python

    from wires import w

    def a_print(*args, **kw):
        print('args=%r kw=%r' % (args, kw))

    w.callable1.wire(a_print, 'one')
    w.callable2.wire(a_print, a='nother')

    w.callable1()                       # prints: args=('one',) kw={}
    w.callable1(42, 24)                 # prints: args=('one', 42, 24) kw={}
    w.callable1(a=42, b=24)             # prints: args=('one',) kw={'a': 42, 'b': 24}
    w.callable1(42, a=24)               # prints: args=('one', 42) kw={'a': 24}

    w.callable2()                       # prints: args=() kw={'a': 'nother'}
    w.callable2(42, 24)                 # prints: args=(42, 24) kw={'a': 'nother'}
    w.callable2(a=42, b=24)             # prints: args=() kw={'a': 42, 'b': 24}
    w.callable2(42, a=24)               # prints: args=(42,) kw={'a': 24}


Unwiring actions can include wire-time arguments in the :meth:`unwire <wires._callable.WiresCallable.unwire>` call:

* If no positional/keyword arguments are passed (other than the mandatory callable argument) the first wiring to that callable is removed.

* If positional/keyword arguments are passed, the specific wiring to that callable with the provided wire-time arguments is removed.

In either case, a :class:`ValueError` is raised when no matching wiring exists.


.. code-block:: python

    from wires import w

    def p_arg(arg):
        print(arg)

    w.callable.wire(p_arg, 'a')
    w.callable()                        # prints 'a'

    w.callable.wire(p_arg, 'b')
    w.callable()                        # prints 'a', then prints 'b'

    w.callable.unwire(p_arg, 'b')
    w.callable()                        # prints 'a'

    w.callable.unwire(p_arg)
    w.callable()                        # does nothing

    w.callable.unwire(p_arg, 'c')       # raises ValueError: no such wiring




Call-time coupling
------------------

.. note::

    For a description of possible behaviours, refer to :ref:`Call-time Coupling Concepts <concepts-calltime-coupling>`.


By default, calling a *wires callable* calls all its wirings and returns ``None``:


.. code-block:: python
    :emphasize-lines: 11

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                     # Default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                    # prints 'about to raise', then 'about to return'
                                    # returns None


Call-time coupling can be:

* Set at the :class:`Wires <wires._wires.Wires>` object level, applicable to all its *wired callables*.
* Overridden on a *wires callable* basis.
* Overridden at call-time.



Setting **returns** at the :class:`Wires <wires._wires.Wires>` object level:

.. code-block:: python
    :emphasize-lines: 11

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires(returns=True)         # Non-default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                    # prints 'about to raise', then 'about to return'
                                    # returns [(ZeroDivisionError(), None), (None, 42)]


Overriding **returns** at the *wires callable* level:

.. code-block:: python
    :emphasize-lines: 11-12

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                     # Default call coupling.
    w.callable.returns = True       # Override call coupling for `callable`.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                    # prints 'about to raise', then 'about to return'
                                    # returns [(ZeroDivisionError(), None), (None, 42)]



Overriding **returns** at call-time:

.. code-block:: python
    :emphasize-lines: 11,16

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                     # Default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w(returns=True).callable()      # Override call coupling at calltime.
                                    # prints 'about to raise', then 'about to return'
                                    # returns [(ZeroDivisionError(), None), (None, 42)]




Setting **ignore exceptions** at the :class:`Wires <wires._wires.Wires>` object level:

.. code-block:: python
    :emphasize-lines: 11

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires(ignore_exceptions=False)  # Non-default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                        # prints 'about to raise' only
                                        # returns None


Overriding **ignore exceptions** at the *wires callable* level:

.. code-block:: python
    :emphasize-lines: 11-12

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                             # Default call coupling.
    w.callable.ignore_exceptions = False    # Override call coupling for `callable`.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                            # prints 'about to raise' only
                                            # returns None



Overriding **ignore exceptions** at call-time:

.. code-block:: python
    :emphasize-lines: 11,16

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                             # Default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w(ignore_exceptions=False).callable()   # Override call coupling at calltime.
                                            # prints 'about to raise' only
                                            # returns None



Setting both **returns** and **ignore exceptions** at the :class:`Wires <wires._wires.Wires>` level:

.. code-block:: python
    :emphasize-lines: 11

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires(returns=True, ignore_exceptions=False)    # Non-default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                        # prints 'about to raise' only
                                        # raises RuntimeError((ZeroDivisionError(), None),)


Overriding both **returns** and **ignore exceptions** at the *wires callable* level:

.. code-block:: python
    :emphasize-lines: 11-13

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                             # Default call coupling.
    w.callable.returns = True               # Override call coupling for `callable`.
    w.callable.ignore_exceptions = False    # Override call coupling for `callable`.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w.callable()                        # prints 'about to raise' only
                                        # raises RuntimeError((ZeroDivisionError(), None),)


Overriding both **returns** and **ignore exceptions** at call-time:

.. code-block:: python
    :emphasize-lines: 11,16

    from wires import Wires

    def raise_exception():
        print('about to raise')
        raise ZeroDivisionError()

    def return_42():
        print('about to return')
        return 42

    w = Wires()                         # Default call coupling.

    w.callable.wire(raise_exception)
    w.callable.wire(return_42)

    w(returns=True, ignore_exceptions=False).callable()
                                        # prints 'about to raise' only
                                        # raises RuntimeError((ZeroDivisionError(), None),)



Introspection
-------------



.. [#wirescallable] Per the :doc:`concepts` section, *wires callables* are :class:`Wires <wires._wires.Wires>` object auto-created attributes.
