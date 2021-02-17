# Frequently Asked Questions
Common fixes to common errors reported by the Community

## AttributeError: 'OWM25' object has no attribute 'xxx' 
Your code looks like:

```python
>>> from pyowm import OWM
>>> owm = OWM('your-api-key-here')
>>> mgr = owm.weather_manager()

AttributeError: 'OWM25' object has no attribute 'weather_manager'
```

This happens because **you are not running PyOWM v3** and this is because  your code is currently **based on an old Python 2 setup**
Python 2 is officially dead and should be removed in favor of Python 3.

What you should do is:
  - install Python 3.6+
  - install PyOWM v3+ with `pip3 install pyowm`

The above snippet should just work fine then. 

Remember to port the rest of your code to Python 3: everything related to PyOWM v2 can be ported using [this guide](https://pyowm.readthedocs.io/en/latest/v3/migration-guide-pyowm-v2-to-v3.md:)

## UnauthorizedError: Invalid API Key provided
You are able to successfully create an `OWM` object and calling functions **other than One-Call** related ones (eg. getting observed or forecasted weather)

As stated in the documentation home page, OpenWeatherMap API recently "blocked" calls towards a few legacy API endpoints whenever requested by **clients using non-recent free API keys.**

This means that PyOWM might return authorization errors in that case.

This behaviour is not showing if you use API keys issued time ago - unfortunately I have no way to be more precise as OWM never stated this officially.

**The proper way to obtain the data you are looking for is to call the "OneCall" PyOWM methods using your API key**

So please refer to the documentation for this


## I cannot use PyOWM 3 so I need to use PyOWM version 2.10
This may happen if you still use Python 2 or you use Python 3 but with a minor version that is not supported by PyOWM
 
Please install PyOWM 2.10 with:
```shell
pip2 install pyowm==2.10 
```

And find the PyOWM 2.10 documentation [here](https://pyowm.readthedocs.io/en/2.10/)


## ModuleNotFound error upon installing PyOWM development branch from Github

Installation of the (potentially unstable) development trunk used to be like this:

```shell
$ pip install git+https://github.com/csparpa/pyowm.git@develop
```

You would get something like:

```shell
Collecting git+https://github.com/csparpa/pyowm.git@develop
  Cloning https://github.com/csparpa/pyowm.git (to revision develop) to /tmp/pip-req-build-_86bl7ty
    [......]
    ERROR: Command errored out with exit status 1:
     command: /home/me/.local/share/virtualenvs/backend-nPPHZqlJ/bin/python -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-req-build-_86bl7ty/setup.py'"'"'; __file__='"'"'/tmp/pip-req-build-_86bl7ty/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base /tmp/pip-pip-egg-info-ww_gs9y3
         cwd: /tmp/pip-req-build-_86bl7ty/
    Complete output (17 lines):
    Traceback (most recent call last):
      [......]
      File "/tmp/pip-req-build-_86bl7ty/pyowm/commons/tile.py", line 6, in <module>
        from pyowm.utils.geo import Polygon
      File "/tmp/pip-req-build-_86bl7ty/pyowm/utils/geo.py", line 4, in <module>
        import geojson
    ModuleNotFoundError: No module named 'geojson'
    ----------------------------------------
ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
```

I've realized this way of installing is bad *as it does not install PyOWM's dependencies** along.
Therefore the right way to go is:

```shell
$ git clone https://github.com/csparpa/pyowm.git
$ cd pyowm && git checkout develop
$ pip install -r requirements.txt && python setup.py install
```    