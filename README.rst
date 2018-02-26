Python Wires: Call wiring made simple
=====================================

.. image:: http://img.shields.io/pypi/v/wires.svg
   :target: https://pypi.python.org/pypi/wires


``wires`` is a library to facilitate "callable wiring" by decoupling callers from callees and avoiding passing around multiple callables in Python code; it can be used as a callable-based event system or, again callable-based, publish-subscribe like solution.

Minimal usage example:

.. code-block:: python

    from wires import wiring, wire

    def my_callable():
        print('Hello from wires!')

    wire.this_callable.calls_to(my_callable)
    wiring.this_callable()



Thanks
------

- Benjamin Peterson and contributors for the `Six <https://pypi.python.org/pypi/six/>`_ Python 2 and 3 Compatibility Library.
- Hynek Schlawack for the articles `Sharing Your Labor of Love: PyPI Quick and Dirty <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>`_ and `Testing & Packaging <https://hynek.me/articles/testing-packaging/>`_.


About
-----

Python Wires was created by Tiago Montes.

