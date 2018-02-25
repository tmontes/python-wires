Python Wires: Call wiring made simple
=====================================

``wires`` is a library to facilitate "callable wiring" by decoupling callers from callees and avoiding passing around multiple callables in Python code. It can be used as a callable-based event system or, again callable-based, publish-subscribe like solution.

Minimal usage example:

.. code-block:: python

    from wires import wire

    def my_callable():
        print('Hello from wires!')

    wire.this.calls_to(my_callable)
    wire.this()



Thanks
======

- Hynek Schlawack for the articles `Sharing Your Labor of Love: PyPI Quick and Dirty <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>`_ and `Testing & Packaging <https://hynek.me/articles/testing-packaging/>`_.


Authors
=======

Tiago Montes

