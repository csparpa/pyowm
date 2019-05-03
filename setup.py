#!/usr/bin/env python

from setuptools import setup
from pyowm import constants
from pyowm.utils.strings import version_tuple_to_str
from pyowm.__version__ import __author__, __author_email__, __description__, __license__, __title__,\
    __url__

setup(
    name=__title__,
    version=version_tuple_to_str(constants.PYOWM_VERSION),
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    packages=['pyowm',
              'pyowm.abstractions',
              'pyowm.agroapi10',
              'pyowm.alertapi30',
              'pyowm.caches',
              'pyowm.commons',
              'pyowm.exceptions',
              'pyowm.pollutionapi30', 'pyowm.pollutionapi30.xsd',
              'pyowm.uvindexapi30', 'pyowm.uvindexapi30.xsd',
              'pyowm.tiles',
              'pyowm.utils',
              'pyowm.weatherapi25', 'pyowm.weatherapi25.cityids', 'pyowm.weatherapi25.xsd',
              'pyowm.stationsapi30', 'pyowm.stationsapi30.xsd'],
    long_description="""PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy 
    consumption of OWM data from Python applications via a simple object model and in a human-friendly fashion.""",
    include_package_data=True,
    install_requires=[
        'requests>=2.20.0,<3',
        'geojson>=2.3.0,<3'
    ],
    python_requires='>=3.4',
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries"],
    package_data={
        '': ['*.gz', '*.xsd', '*.md', '*.txt', '*.json']
    },
    keywords='openweathermap web api client weather forecast uv alerting owm pollution meteostation agro agriculture',
    license=__license__
)
