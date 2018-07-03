.. pyowm documentation master file, created by
   sphinx-quickstart on Thu Aug 25 12:34:05 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyOWM
=====

Welcome to PyOWM's documentation!

What is PyOWM?
--------------

PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy
consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.


What APIs does PyOWM allow me to use?
-------------------------------------

With PyOWM you can interact programmatically with the following OpenWeatherMap web APIs:

 - Weather API v2.5
 - Pollution API v3.0
 - Stations API v3.0
 - Weather Alerts API v3.0

and more will be supported in the future. Stay tuned!


Supported environments and Python versions
------------------------------------------

PyOWM runs on Windows, Linux and MacOS.

PyOWM runs on:

  - Python 2.7
  - Python 3.4+

**Please notice that support for Python 2.x will eventually be dropped - check details_

.. _details: https://github.com/csparpa/pyowm/wiki/Timeline-for-dropping-Python-2.x-support


PyOWM also integrates with Django_ 1.10+ models, but that integration might have issues (contributions are welcome)

.. _Django: https://github.com/csparpa/pyowm/wiki/Django-support


Installation
------------

pip
~~~

The easiest method of all:

.. code::

    $ pip install pyowm

Get the lastest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install the development trunk with _pip_:

.. code::

    $ pip install git+https://github.com/csparpa/pyowm.git@develop


but be aware that it might not be stable!


setuptools
~~~~~~~~~~

Please see here_

.. _here: https://github.com/csparpa/pyowm/wiki/Install#install-from-source-with-setuptools)

Distribution packages
~~~~~~~~~~~~~~~~~~~~~

  - On Windows you have installers_
      .. _installers: https://github.com/csparpa/pyowm/wiki/Install#windows-exe
  - On ArchLinux you can install PyOWM from Yaourt_
      .. _Yaourt: https://github.com/csparpa/pyowm/wiki/Install#on-archlinux-with-yaourt



Examples and Guides
-------------------

.. toctree::
   :maxdepth: 1

   object-model
   usage-examples
   air-pollution-api-usage-examples
   uv-api-usage-examples


PyOWM software API documentation
--------------------------------

Contents:

.. toctree::
   :maxdepth: 1

   pyowm


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

