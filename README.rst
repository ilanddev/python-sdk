===============================
iland-sdk
===============================

.. image:: https://img.shields.io/pypi/v/iland-sdk.svg
        :target: https://pypi.python.org/pypi/iland-sdk

.. image:: https://travis-ci.org/ilanddev/python-sdk.svg?branch=master
        :target: https://travis-ci.org/ilanddev/python-sdk

.. image:: https://readthedocs.org/projects/iland-sdk/badge/?version=latest
        :target: https://readthedocs.org/projects/iland-sdk/?badge=latest
        :alt: Documentation Status


iland cloud Python SDK

* Free software: BSD License
* Documentation: https://iland-sdk.readthedocs.org.
* iland cloud API doc: https://api.ilandcloud.com.

============
Introduction
============

This library provides a pure Python interface for the `iland cloud API
<https://www.iland.com/>`_. It works with Python versions from 2.7+.

`iland cloud <http://www.iland.com>`_ provides Enterprise-grade IaaS and this
library is intended to make it even easier for Python programmers to use.

================
Getting the code
================

The code is hosted at https://github.com/ilanddev/python-sdk

Check out the latest development version anonymously with::

    $ git clone https://github.com/ilanddev/python-sdk.git
    $ cd python-sdk

==========
Installing
==========

You can install iland-sdk from Pypi using::

    $ pip install iland-sdk

You can also install it using actual checkout::

    $ git clone https://github.com/ilanddev/python-sdk.git

    $ cd python-sdk

    $ pip install -e .

=============
Running Tests
=============

To run the unit tests::

	$ make test

To run the unit tests for all supported Python interpreters::

    $ make test-all

To check your changes::

    $ make lint

---
API
---

The API is exposed via the ``iland.Api`` class.

To create an instance of the ``iland.Api``::

    >>> import iland
    >>> api = iland.Api(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        username=USERNAME,
                        password=PASSWORD)

You can then perform GET, PUT, PUSH and DELETE requests against the iland
cloud::

    >>> api.get('/user/' + USERNAME)
    >>> user.get('name'))
    USERNAME

    >>> user_alert_emails = {'emails': ['test@iland.com', 'test2@iland.com'],
                             'username': USERNAME}
    >>> api.post('/user/' + USERNAME + '/alert-emails', user_alert_emails)


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
