Development
===========

Python Wires is openly developed at https://github.com/tmontes/python-wires, following a process that strives to be:

* As simple as possible, but not simpler.
* Easy to understand.
* Structured.
* Flexible.

Substantiated contributions and discussions on this topic will be welcome.



Development Environment
-----------------------

*write me*

.. code-block:: console

    $ git clone https://github.com/tmontes/python-wires
    $ cd python-wires/
    $ pip install -e .[dev]


*write me before coverage*

.. code-block:: console

    $ coverage run -m unittest discover
    $ coverage report


*write me before tox*

.. code-block:: console

    $ pip install tox
    $ tox



Process Overview
----------------

Milestones
^^^^^^^^^^

The following `milestones <https://github.com/tmontes/python-wires/milestones>`_ are tracked:

==========  ================================================================================
**NEXT**    Issues and Pull Requests that will be included in the next release.
**DEFER**   Issues and Pull Requests that will be worked on, but will not be included in the next release.
**TBD**     Issues and Pull Requests that will not be worked on until future decision.
==========  ================================================================================

.. note::
    Unassigned Issues and Pull Requests will be assigned to the **TBD** milestone.

At release time:

* The **NEXT** milestone is renamed to the release version and closed.
* A new **NEXT** milestone is created, with no associated Issues or Pull Requests.



Issues
^^^^^^

All development issues will be `labelled <https://github.com/tmontes/python-wires/labels>`_ one of:

=============== =================================================================================
**enhancement** Describing a new feature or capability.
**bug**         Describing something that isn't working as documented.
**develop**     Describing other development related issues: refactors, automation, process, etc.
=============== =================================================================================


.. note::
    The key motivation for having mandatory labels in development issues is to simplify filtering support related ones which submitters will tend to leave unlabelled.


General requirements:

* All issues must describe a single, actionable topic.

* Complex issues should be split into simpler, possibly related, issues.

* **enhancement** issues:

  * Must describe the use-case, benefits and tradeoffs.

  * Should include sample code demonstrating the enhancement in action.

  * Should take the `Checklist for Python library APIs <http://python.apichecklist.com>`_ into consideration.

* **bug** issues must:

  * Be explicitly reported against either the latest `PyPI released version <https://pypi.python.org/pypi/wires>`_ or the current `GitHub master branch <https://github.com/tmontes/python-wires/tree/master>`_.

  * Describe the steps to reproduce the bug, ideally with a minimal code sample.

  * Describe the expected and actual results.

  * Include a reference to where the documentation is inconsistent with the actual results.


* **development** issues:

  * Must describe the purpose, benefits and trade-offs.


.. warning::
    Open development issues not fulfilling these requirements will be either discarded and closed, or worked on, at the maintainer's discretion.



Pull Requests
^^^^^^^^^^^^^

Pull Requests are `tracked here <https://github.com/tmontes/python-wires/pulls>`_ and:

* Must reference an existing, open issue, and preferably only one.
* May totally or partially contribute to closing the referenced open issue.
* Will not be merged if any of the GitHub checks fails.
* Will not necessarily be merged if all of the GitHub checks pass.
* Must be assigned to the same milestone as the referenced open issue.
* May be labelled.


