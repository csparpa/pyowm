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

This behaviour is not showing if you use API keys issued time ago - unfortunately I have no wasy to be more precise as OWM never stated this officially.

**The proper way to obtain the data you are looking for is to call the "OneCall" PyOWM methods using your API key**

So please refer to the documentation for this


## I cannot use PyOWM 3 so I need to use PyOWM version 2.10
This may happen if you still use Python 2 or you use Python 3 but with a minor version that is not supported by PyOWM
 
Please install PyOWM 2.10 with:
```shell
pip2 install pyowm==2.10 
```

And find the PyOWM 2.10 documentation [here](https://pyowm.readthedocs.io/en/2.10/)