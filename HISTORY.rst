=======
History
=======

0.7.3 (2017-05-17)
------------------

* Lower required version of `requests` module from `==2.14.2` to `>=2.2.1`.

0.7.2 (2017-05-16)
------------------

* optional `access_url_token` `Api` constructor param allowing one to override
  token exchange URL.
* update dependencies.

0.7.1 (2017-02-08)
------------------

* update outdated dependencies
* drop Python 3.3 support "just like everybody"
* update token exchange endpoint. We keeping BBB for old client implementations

0.7.0 (2016-10-13)
------------------

* update token exchange endpoint. We keeping BBB for old client implementations
* update requests lib
* update dev dependencies
* promote to stable

0.6.0 (2016-6-28)
-----------------

* update dependencies
* default resource path update

0.5.0 (2016-3-22)
-----------------

* promote to beta status
* extra `verify_ssl` `Api` constructor to allow one to not verify endpoints SSL

0.4.0 (2016-3-08)
-----------------

* support 204 no content HTTP return code
* fix naming of _validate_token method
* update Sphynx dependency
* full unit tests coverage
* fix return on POST, PUT and DELETE operations
* fix use of custom BASE API URL

0.3.0 (2016-2-18)
-----------------

* implement exceptions handling
* docstrings and documentation
* Housekeeping and refactoring
* Better CI setup
* Sphynx doc and readthedocs.org publishing.

0.2.0 (2016-2-09)
-----------------

* Minor fixes.

0.1.0 (2016-2-09)
-----------------

* First release on PyPI.
