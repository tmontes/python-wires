Python Wires: Simple Callable Wiring
====================================

.. image:: http://img.shields.io/pypi/v/wires.svg
   :target: https://pypi.python.org/pypi/wires
   :alt: PyPI

.. image:: https://img.shields.io/travis/tmontes/python-wires.svg
   :target: https://travis-ci.org/tmontes/python-wires
   :alt: CI Status

.. image:: https://codecov.io/github/tmontes/python-wires/branch/master/graph/badge.svg
   :target: https://codecov.io/github/tmontes/python-wires
   :alt: Test Coverage

.. image:: https://readthedocs.org/projects/python-wires/badge/?version=latest
   :target: https://python-wires.readthedocs.io/
   :alt: Documentation


|


Python Wires is a library to facilitate callable wiring by decoupling callers from callees. It can be used as a simple callable-based event notification system, as an in-process publish-subscribe like solution, or in any use case where callable chaining and decoupling is appropriate.

Quick Start
-----------

Start off by creating a ``Wiring`` object:

.. code-block:: python

    from wires import Wiring

    w = Wiring()

``Wiring`` object attributes are callables, auto-created on first access; each such callable can be wired to other, existing, callables:


.. code-block:: python

    def say_hello():
        print('Hello from wires!')

    w.my_callable.wire(say_hello)       # Wire `say_hello` to `w.my_callable`.


Calling a ``Wiring`` callable attribute calls its wired callables:

.. code-block:: python

    w.my_callable()                     # Prints 'Hello from wires!'


Wiring multiple callables 

.. code-block:: python

    def say_bye():
        print('Bye bye!')

    w.my_callable.wire(say_bye)         # Also wire `say_bye` to `w.my_callable`.
    w.my_callable('world!')             # Now prints 'Hello world!' and 'Bye bye world!'.



.. marker-end-welcome-dont-remove


Full documentation at https://python-wires.readthedocs.org/.




Thanks
------

.. marker-start-thanks-dont-remove

- Hynek Schlawack for the articles `Sharing Your Labor of Love: PyPI Quick and Dirty <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>`_ and `Testing & Packaging <https://hynek.me/articles/testing-packaging/>`_.

- Stuart Colville for the article `Including parts of README.rst in your sphinx docs <https://muffinresearch.co.uk/selectively-including-parts-readme-rst-in-your-docs/>`_.

.. marker-end-thanks-dont-remove



About
-----

.. marker-start-about-dont-remove

Python Wires was created by Tiago Montes.

.. marker-end-about-dont-remove

