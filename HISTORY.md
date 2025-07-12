## History

1.0.0
----------------------
* Switched from unify to string_fixer for quote style formatting, since unify doesn't work in Python 3.11+

0.16.0
----------------------
* Bump `rich` version

0.15.0
----------------------
* Add support for isort add-imports and remove-imports features (by [@sodul](https://github.com/sodul))

0.14.0
----------------------
* Drop support for Python 3.7, add support for Python 3.12, upgrade ifixit to v2 (by [@sodul](https://github.com/sodul))


0.13.0
----------------------
* Add support for Python 3.11 (by [@mosquito](https://github.com/mosquito))


0.12.0
----------------------

* Add support to exclude files and folders (by [@sodul](https://github.com/sodul))
  Potential backward compatibility issue with the default exclusion list.
  Some files and folders might now be excluded while they would have been
  processed in older versions.
* remove travis.yml since it is no longer usable.


0.11.0
----------------------

* Add GitHub Action to validate PRs (by [@sodul](https://github.com/sodul))
* Update third party requirements (by [@sodul](https://github.com/sodul))
* Drop support for Python 3.6 (by [@sodul](https://github.com/sodul))


0.10.0
----------------------

* [black](https://github.com/psf/black) support (by [@sodul](https://github.com/sodul))


0.9.0
----------------------

* update python dependencies


0.8.1
----------------------

* Add support for python 3.9


0.8.0
----------------------

* [fixit](https://github.com/Instagram/Fixit) support


0.7.0
----------------------

* [pre-commit](https://pre-commit.com/) support (by [@tzoiker](https://github.com/tzoiker))


0.6.2
----------------------

* isort: keep line breaks before local imports


0.6.1
----------------------

* Fix isort imports grouping


0.6.0
----------------------

* Bump isort to 5.4.2
* Use parentheses in multiline imports


0.5.0
----------------------

* Add autoflake formatter
* Add trim formatter


0.4.0
----------------------

* Minimum python version option
* Pyupgrade options
* Detecting and skipping virtualenv


0.3.0
----------------------

* Multiprocessing support (by [@mosquito](https://github.com/mosquito))


0.2.0
-----------------------

* Pre-commit hook
* Some formating options


0.1.0 (2020-04-06)
------------------------

* First release on PyPI.
