.. pyowm documentation master file, created by
   sphinx-quickstart on Thu Aug 25 12:34:05 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyOWM
=====

Welcome to PyOWM v3 documentation!

.. image:: ../logos/180x180.png
   :width: 180px
   :height: 180px
   :scale: 100 %
   :alt: PyOWM
   :align: center


What is PyOWM?
--------------

PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy
consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.


What APIs can I access with PyOWM?
----------------------------------

With PyOWM you can interact programmatically with the following OpenWeatherMap web APIs:

 - **Weather API v3.0** + **OneCall API**, offering
    + current weather data
    + weather forecasts
    + weather history
 - **Agro API v1.0**, offering polygon editing, soil data, satellite imagery search and download
 - **Air Pollution API v3.0**, offering data about CO, O3, NO2 and SO2
 - **UV Index API v3.0**, offering data about Ultraviolet exposition
 - **Stations API v3.0**, allowing to create and manage meteostation and publish local weather measurements
 - **Weather Alerts API v3.0**, allowing to set triggers on weather conditions and areas and poll for spawned alerts
 - **Geocoding API v1.0** allowing to perform direct/reverse geocoding

And you can also get **image tiles** for several map layers provided by OWM


The documentation of OWM APIs can be found on the OWM Website_

.. _Website: https://openweathermap.org/api



Very important news
~~~~~~~~~~~~~~~~~~~
OpenWeatherMap API recently "blocked" calls towards a few legacy API endpoints whenever requested by **clients using non-recent free API keys.**

This means that if you use PyOWM methods such as the ones for getting observed or forecasted weather, PyOWM might return authorization errors
This behaviour is not showing if you use API keys issued a long time ago.

*The proper way to obtain such data is to call the "OneCall" methods using your API key*


Used to work with PyOWM v2?
---------------------------

PyOWM v3 is a brand new branch of the library and therefore differs from PyOWM v2 branch.
This means that **v3 offers no retrocompatibility with v2: this might result in your code breaking** if
it uses PyOWM v2 and you uncarefully update!
Moreover, PyOWM v3 runs on Python 3 only.

PyOWM v2 will follow this Timeline_

It is highly recommended that you upgrade your PyOWM v2 dependency to PyOWM v3: follow this guide for Migrating_


.. _Timeline: v3/maintenance-streams-timelines.html
.. _Migrating: v3/migration-guide-pyowm-v2-to-v3.html


Supported environments and Python versions
------------------------------------------

PyOWM runs on Windows, Linux and MacOS.
PyOWM runs on Python 3.7+


Usage and Technical Documentation
---------------------------------

PyOWM v3 documentation
~~~~~~~~~~~~~~~~~~~~~~

Quick code recipes
^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/code-recipes


FAQ about common errors
^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/faq



PyOWM v3 software API documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is the Python API documentation of PyOWM:

.. toctree::
   :maxdepth: 1

   pyowm

Description of PyOWM configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/pyowm-configuration-description


Global PyOWM instantiation documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/global-pyowm-usage-examples


City ID registry documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/city-id-registry-examples


Weather API examples
^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/weather-api-usage-examples

Agro API examples
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   v3/agro-api-usage-examples


UV API examples
^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/uv-api-usage-examples


Air Pollution API examples
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   v3/air-pollution-api-usage-examples

Stations API examples
^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/stations-api-usage-examples

Alerts API examples
^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/alerts-api-usage-examples

Geocoding API examples
^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   v3/geocoding-api-usage-examples


Map tiles client examples
^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/map-tiles-client-usage-examples.md

PyOWM Exceptions
^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/exceptions.md

Utility functions examples
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. toctree::
   :maxdepth: 1

   v3/utilities-usage-examples.md


Legacy PyOWM v2 documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Please refer to historical archives on Readthedocs or the GitHub repo for this


Installation
------------

pip
~~~

The easiest method of all:

.. code::

    $ pip install pyowm

If you already have PyOWM 2.x installed and want to upgrade to safely update it to the latest 2.x release just run:

.. code::

    $ pip install --upgrade pyowm>=2.0,<3.0


Get the latest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install the development trunk with _pip_:

.. code::

    git clone https://github.com/csparpa/pyowm.git
    cd pyowm && git checkout develop
    pip install -r requirements.txt  # install dependencies
    python setup.py install          # install develop branch code


but be aware that it might not be stable!

setuptools
~~~~~~~~~~

You can install from source using _setuptools_: either download a release from GitHub or just take the latest main branch), then:

.. code::

   $ unzip <zip archive>   # or tar -xzf <tar.gz archive>
   $ cd pyowm-x.y.z
   $ python setup.py install

The .egg will be installed into the system-dependent Python libraries folder


Distribution packages
~~~~~~~~~~~~~~~~~~~~~

On Windows you have EXE installers

On ArchLinux you can use the Yaourt package manager, run:

.. code::

   Yaourt -S python2-owm  # Python 2.7 (https://aur.archlinux.org/packages/python-owm)
   Yaourt -S python-owm   # Python 3.x (https://aur.archlinux.org/packages/python2-owm)

On OpenSuse you can use with YaST/Zypper package manager, run:

.. code::

   zypper install python-pyowm


How to contribute
-----------------
There are multiple ways to contribute to the PyOWM project! Find the one that suits you best

.. toctree::
   :maxdepth: 1

   contributing


PyOWM Community
---------------
Find us on Slack_ !

.. _Slack: http://pyowm-slackin.herokuapp.com/



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

