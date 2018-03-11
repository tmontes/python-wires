Python Wires: Simple Call Wiring
================================

.. image:: http://img.shields.io/pypi/v/wires.svg
   :target: https://pypi.python.org/pypi/wires
   :alt: PyPI

.. image:: https://img.shields.io/travis/tmontes/python-wires.svg
   :target: https://travis-ci.org/tmontes/python-wires
   :alt: CI Status

.. image:: https://codecov.io/github/tmontes/python-wires/branch/master/graph/badge.svg
   :target: https://codecov.io/github/tmontes/python-wires
   :alt: Test Coverage


|


``wires`` is a library to facilitate "call wiring" by decoupling callers from callees; it can be used as a callable-based event system or publish-subscribe like solution.

Minimal example:

.. code-block:: python

    from wires import w

    def my_callable():
        print('Hello from wires!')

    w.this_callable.wire(my_callable)
    w.this_callable()



Thanks
------

- Hynek Schlawack for the articles `Sharing Your Labor of Love: PyPI Quick and Dirty <https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/>`_ and `Testing & Packaging <https://hynek.me/articles/testing-packaging/>`_.


About
-----

Python Wires was created by Tiago Montes.

