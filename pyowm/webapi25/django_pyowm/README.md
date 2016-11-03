# django-pyowm

This Django project contains a reusable app providing a Django ORM interface 
to operate with PyOWM domain entities for OWM API version 2.5

The app is named `pyowm_models`

## Django support
The app works with Django 1.10+ and Python 2.7 or 3.2+


## Install
You can either reuse this Django project as a template to develop your
own one, or reuse the `pyowm_models` app.

To do so, you need to install PyOWM first (eg: using `pip`) and then
add `pyowm_models` to the `INSTALLED_APPS` list into your Django
 project's `settings.py` file:
 
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pyowm.webapi25.django_pyowm.pyowm_models'  # <---
]
```


You can now import PyOWM models into your code and use them.

## Features
Models behave as all other Django models but they have a few useful 
functions:

  -  `<Model_class>.from_entity(entity)` - creates a PyOWM model instance
     from the corresponding PyOWM domain object instance
  -  `<Model_instance>.to_entity(entity)` - turns the model instance to
     the corresponding PyOWM domain object instance

## Usage

In your own Django project's code you can do something like this:

```python
from pyowm import OWM
from pyowm.webapi25.django_pyowm.pyowm_models import models

# Get data an Observation from the API 
owm = OWM(API_key='my_key')
obs = owm.weather_at_place('London,UK')

# Create a model instance from API response
m = models.Observation.from_entity(obs)

# Save related objects and then the model itself
m.location.save()
m.weather.save()
m.save()

# .. or save everything in one shot
m.save_all()

# From model instance to entity
original_obs = m.to_entity()
```