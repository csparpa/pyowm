#!/usr/bin/env python

from setuptools import setup, find_packages
from pyowm.__version__ import __author__, __author_email__, __description__, __license__, __title__,\
    __url__, __version__

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name=__title__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    packages=find_packages(exclude=['tests','tests.*']),
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'requests>=2.20.0,<3',
        'geojson>=2.3.0,<3',
        'PySocks>=1.7.1,<2',
        'requests[socks]'
    ],
    python_requires='>=3.7',
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.7",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries"],
    package_data={
        '': ['*.bz2', '*.md', '*.txt', '*.json']
    },
    keywords='openweathermap web api client weather forecast uv alerting owm pollution meteostation agro agriculture',
    license=__license__
)
