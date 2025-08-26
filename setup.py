#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='pyowm',
    version='3.5.0',
    description='A Python wrapper around OpenWeatherMap web APIs',
    author='Claudio Sparpaglione',
    author_email='csparpa@gmail.com',
    url='https://github.com/csparpa/pyowm',
    packages=find_packages(exclude=['tests','tests.*']),
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        "requests[socks]>=2.20.0,<3",
        "geojson>=2.3.0,<4",
        "PySocks>=1.7.1,<2",
        "importlib_resources; python_version < '3.12'"
    ],
    python_requires='>=3.9',
    classifiers=[
      "License :: OSI Approved :: MIT License",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
      "Programming Language :: Python :: 3.13",
      "Natural Language :: English",
      "Operating System :: OS Independent",
      "Development Status :: 5 - Production/Stable",
      "Intended Audience :: Developers",
      "Topic :: Software Development :: Libraries"],
    package_data={
        '': ['*.bz2', '*.md', '*.txt', '*.json']
    },
    keywords='openweathermap web api client weather forecast uv alerting owm pollution meteostation agro agriculture',
    license='MIT'
)
