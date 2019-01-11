Python Wires: Simple Callable Wiring
====================================

.. image:: http://img.shields.io/pypi/v/wires.svg
   :target: https://pypi.org/pypi/wires
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


Python Wires is a library to facilitate callable wiring by decoupling callers from callees. It can be used as a simple callable-based event notification system, as an in-process publish-subscribe like solution, or in any context where 1:N callable decoupling is appropriate.


Installation
------------

Python Wires is a pure Python package distributed via `PyPI <https://pypi.org/pypi/wires>`_. Install it with:

.. code-block:: console

	$ pip install wires



Quick Start
-----------

Create a ``Wires`` object:

.. code-block:: python

    from wires import Wires

    w = Wires()

Its attributes are callables, auto-created on first access, that can be wired to other callables:


.. code-block:: python

    def say_hello():
        print('Hello from wires!')

    w.my_callable.wire(say_hello)       # Wires `w.my_callable`, auto-created, to `say_hello`.


Calling such callables calls their wired callables:

.. code-block:: python

    w.my_callable()                     # Prints 'Hello from wires!'


More wirings can be added:

.. code-block:: python

    def say_welcome():
        print('Welcome!')

    w.my_callable.wire(say_welcome)     # Wires `w.my_callable` to `say_welcome`, as well.
    w.my_callable()                     # Prints 'Hello from wires!' and 'Welcome!'.


Wirings can also be removed:

.. code-block:: python

    w.my_callable.unwire(say_hello)     # Removes the wiring to `say_hello`.
    w.my_callable()                     # Prints 'Welcome!'

    w.my_callable.unwire(say_welcome)   # Removes the wiring to `say_welcome`.
    w.my_callable()                     # Does nothing.


To learn more about Python Wires, including passing parameters, setting wiring limits and tuning the call-time coupling behaviour, please refer to the remaining documentation at https://python-wires.readthedocs.org/.

.. marker-end-welcome-dont-remove


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

