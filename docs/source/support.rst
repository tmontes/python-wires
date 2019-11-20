Support
=======

Python Wires support is based on volunteer effort, delivered on an availability and best-effort basis.


Versions and Platforms
----------------------

Following a strict `Backwards Compatibility Policy`_, Python Wires strives to work on as many Python interpreters and underlying platforms as possible. For that, care is taken in crafting and maintaining a clean, documented code base, that respects and uses safe, non-deprecated Python programming APIs and conventions.

There is, however, a limited set of interpreters and platforms where development and automated testing takes place; these are the only ones where, respectively, human based diagnostics are completed, and where "correctness assertions" [#correctness]_ can be made.

.. important::

    For these motives, the only supported version is the latest `PyPI released version <https://pypi.org/pypi/wires>`_, running on an interpreter and platform for which automated testing is in place:

    * CPython 2.7 on 64 bit Linux, Windows or macOS systems.
    * CPython 3.6 on 64 bit Linux, Windows or macOS systems.
    * CPython 3.7 on 64 bit Linux, Windows or macOS systems.
    * CPython 3.8 on 64 bit Linux, Windows or macOS systems.

    Other interpreters and platforms may become supported in the future.

Python Wires versions follow a `Calendar Versioning <https://calver.org/>`_ scheme with :guilabel:`YY.MINOR.MICRO` tags, where:

=================== ============================================================
:guilabel:`YY`      Is the two digit year of the release.
:guilabel:`MINOR`   Is the release number, starting at 1 every year.
:guilabel:`MICRO`   Is the bugfix release, being 0 for non-bugfix only releases.
=================== ============================================================



Backwards Compatibility Policy
------------------------------

* A given release is API compatible with the release preceding it, possibly including new backwards-compatible features: codebases depending on a given Python Wires release should be able to use a later release, with no changes.

* Notable exceptions:

  * Bug fixes may change an erroneous behaviour that a codebase oddly depends on.

  * Deprecations, as described below.



Deprecation Policy
------------------

If a non-backwards compatible API change is planned:

* A fully backwards compatible release will be made, where uses of API about to break compatibility will issue ``WiresDeprecationWarning``\s using the Python Standard Library's `warnings <https://docs.python.org/3/library/warnings.html>`_ module as in:

    .. code-block:: python

        import warnings

        class WiresDeprecationWarning(DeprecationWarning):
            pass

        warnings.simplefilter('always', WiresDeprecationWarning)
        warnings.warn('message', WiresDeprecationWarning)

* A non-backwards compatible release will be made, no earlier than six months after the release including the ``WiresDeprecationWarning``\s.



Requesting Support
------------------

Before moving forward, please review the documentation: it may include the answers you're looking for. After that, if still in need of support, `take this guide into consideration <https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution>`_, and then open a new issue `here <https://github.com/tmontes/python-wires/issues/new>`_, taking care to submit:

* A clear and concise summary.
* A detailed description, including snippets of code, if considered useful.

If something is not working as expected, please also include:

* A short code sample demonstrating the behaviour, along with the actual and expected results.
* The Python Wires version (eg. 18.1.0).
* The Python interpreter version (eg. CPython 3.5.2 64 bit).
* The operating system version (eg. Debian 9 "stretch" 64 bit).

.. note::
    Addressing requests targeting unsupported versions, interpreters or platforms may require additional efforts and non-trivial amounts of time. Besides that, they will be equally welcome.


.. [#correctness] Whatever that means, without implying any guarantees other than the ones expressed in the :doc:`license`.

