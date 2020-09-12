pyenv-api - A simple API for pyenv
======================================

|Build Status|
|Latest Version|
|Support|
|MIT License|

This package provides an API in the form of a wrapper around `pyenv`_. It can be used to install, uninstall and switch Python versions.

Note: This document is based on `virtualenv-api README`_.

.. _pyenv: https://github.com/pyenv/pyenv
.. _virtualenv-api README: https://github.com/sjkingo/virtualenv-api/blob/master/README.rst
.. |Build Status| image:: https://api.travis-ci.org/ulacioh/pyenv-api.svg
   :target: https://travis-ci.org/github/ulacioh/pyenv-api
.. |Latest Version| image:: https://img.shields.io/pypi/v/pyenv-api
   :target: https://pypi.org/project/pyenv-api/
.. |Support| image:: https://img.shields.io/pypi/pyversions/pyenv-api
   :target: https://www.python.org/
.. |MIT License| image:: https://img.shields.io/github/license/ulacioh/pyenv-api
   :target: https://github.com/ulacioh/pyenv-api/blob/master/LICENSE


Installation
------------

The latest stable release is available on `PyPi`_:

::

    $ pip install pyenv-api

Please note that the distribution is named ``pyenv-api``, yet the Python
package is named ``pyenvapi``.

Alternatively, you may fetch the latest version from git:

::

    $ pip install git+https://github.com/ulacioh/pyenv-api.git

.. _PyPi: https://pypi.org/project/pyenv-api/

Usage
-----

pyenvapi package provides a class named ``PyenvAPI`` that lets to interact, through his methods, with pyenv subcommands and options:

.. code:: python

    from pyenvapi import PyenvAPI
    
    pyenv = PyenvAPI()

Note: if `pyenv`_ utility is not installed on your system when you will try to get a ``PyenvAPI`` instance, a ``NotInstalledError`` would be raised.

.. _pyenv: https://github.com/pyenv/pyenv

Operations
----------

Once you have a ``PyenvAPI`` object, you can perform operations on it.

- Get a tuple of versions installed via pyenv itself:

.. code:: python

    >>> pyenv.installed
    ('2.7.2', '3.7.0', '3.8.0')

-  Get, set and unset the global Python version:

.. code:: python

    >>> pyenv.global_version # Get
    ('system',)
    
    >>> pyenv.global_version = ('3.8.0',) # Set
    
    # You can also set more than one version as global
    # or use a list:
    >>> pyenv.global_version = ['2.7.2', '3.8.0']
    
    >>> del pyenv.global_version # Unset
    # This last example set the 'system' version as global.

-  Get a tuple of available Python versions to install:

.. code:: python

    >>> pyenv.available
    ('Python versions tuple, too many versions...',)

-  Install a Python version:

   `Read about subprocess.Popen objects`_

   .. _Read about subprocess.Popen objects: https://docs.python.org/3/library/subprocess.html#popen-objects

.. code:: python

    >>> ps = pyenv.install('3.6.0')
    # `install` method returns a `subprocess.Popen` object
    
    >>> type(ps)
    <class 'subprocess.Popen'>

-  Uninstall a Python version:

.. code:: python

    >>> ps = pyenv.uninstall('3.6.0')
    # `uninstall` method returns a tuple with
    # information of the terminated child process.
    
    >>> returncode, stdout, stderr = ps
    # `returncode` - Exit status of the child process
    # `stdout` - A bytes sequence of the captured stdout
    # `stderr` - A bytes sequence of the captured stderr

TODO
------------
* Add support for pyenv-win
* ...
