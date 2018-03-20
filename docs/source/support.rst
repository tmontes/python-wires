Support
=======

Python Wires support is based on volunteer effort, delivered on an availability and best-effort basis.


Versions and Platforms
----------------------

Following a strict `Backwards Compatibility Policy`_, Python Wires strives to work on as many Python interpreters and underlying platforms as possible. For that, care is taken in crafting and maintaining a clean, documented code base, that respects and uses safe, non-depcrecated Python programming APIs and conventions.

There is, however, a limited set of interpreters and platforms where development and automated testing takes place, under which "correctness assertions" [#correctness]_ and human based diagnostics can take place.

.. important::

    For these motives, the only supported version is the latest `PyPI released version <https://pypi.python.org/pypi/wires>`_, running on an interpreter and platform for which automated testing is in place:

    * CPython 2.7 on a glibc based Linux system.
    * CPython 3.6 on a glibc based Linux system.

    Other interpreters and platforms may become supported in the future.

Python Wires versions follow a `Calendar Versioning <https://calver.org/>`_ scheme with :guilabel:`YY.MINOR.MICRO` tags, where:

=================== ============================================================
:guilabel:`YY`      Is the two digit year of the release.
:guilabel:`MINOR`   Is the release number, starting at 1 every year.
:guilabel:`MICRO`   Is the bugfix release, being 0 for non-bugfix only releases.
=================== ============================================================



Backwards Compatibility Policy
------------------------------

* A given release is API compatible with the release preceeding it, possibly including new backwards-compatible features: codebases depending on a given Python Wires release should be able to use a later release, with no changes.

* Notable exceptions:

  * Bug fixes may change an erroneous behaviour that a codebase oddly depends on.

  * Deprecations, as described below.



Deprecation Policy
------------------

If a non-backwards compatible API change is planned:

* A fully backwards compatible release will be made, where uses of API about to break compatibility will issue ``WiresDeprecationWarning``\s using the Python Standard Library's `warnings <https://docs.python.org/3.6/library/warnings.html>`_ module as in:

    .. code-block:: python

        import warnings

        class WiresDeprecationWarning(DeprecationWarning):
            pass

        warnings.simplefilter('always', WiresDeprecationWarning)
        warnings.warn('message', WiresDeprecationWarning)

* A non-backwards compatible release will be made, no earlier than six months after the release including the ``WiresDeprecationWarning``\s.



Requesting Support
------------------

asdasdasd



.. [#correctness] Whatever that means, without implying any guarantees other than the ones expressed in the :doc:`license`.

