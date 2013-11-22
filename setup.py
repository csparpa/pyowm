#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyowm',
    version='0.2.0',
    description='A Python wrapper around the OpenWeatherMap API',
    author='Claudio Sparpaglione (@csparpa)',
    author_email='claspock@hotmail.com',
    url='http://github.com/csparpa/pyowm',
    packages=['pyowm','pyowm.abstractions', 'pyowm.commons', 'pyowm.exceptions',
              'pyowm.utils', 'pyowm.webapi25', 'tests.unit', 'tests.functional'],
      long_description="""\
      PyOWM is a client Python wrapper library for the OpenWeatherMap v2.5 web API.
      It allows quick and easy consumption of OWM weather data (either observations
      and forecast) from Python applications via a simple object model.
      """,
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Topic :: Software Development :: Libraries",
    ],
    keywords='openweathermap api wrapper weather data OWM',
    license='MIT',
    test_suite='tests'
)
