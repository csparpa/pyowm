# PyOWM v2 to v3 migration guide

## Scenario
You have PyOWM v2.x installed and your code uses it.

## Goal
You want to swap in PyOWM v3.x and swap out PyOWM v2.x

## Steps

  1. Is your code running on Python < 3 ? If so, migrate your code to Python 3 and then resume from here
  2. If you package and distribute PyOWM as a dependency of your code using please correct the PyOWM version: this includes patching `setup.py`, `Pipfile`, `requirements.txt` or any other mechanism you use to declare the dependency.
  Example for `requirements.txt`: from
  
  ```
  pyowm==2.10
  ```
  
  to
  
  ```
  pyowm>=3
  ```
  3. If you have tests for your code then you have a very good way to check that the PyOWM version update won't break your code. If you don't, then you might be at risk - this is a good time to start testing your stuff :-)
  4. Check all lines in your code that invoke PyOWM by reading and comparing the v2 and the v3 documentation - and patch the calls wherever they broke!
  5. Dry run your code
