# PyOWM configuration description

PyOWM can be configured at your convenience.

The library comes with a pre-cooked configuration that you can change according to your needs. The configuration is formulated as a Python dictionary.

## Default configuration
The default config is the `DEFAULT_CONFIG` dict living in the `pyowm.config` module (check it to know the defaults) 

## Configuration format
The config dict is formatted as follows:

```
{
    "subscription_type": <pyowm.commons.enums.SubscriptionTypeEnum>,
    "language": <str>,
    "connection": {
        "use_ssl": <bool>
        "verify_ssl_certs": <bool>,
        "use_proxy": <bool>,
        "timeout_secs": <int>,
        "max_retries": <int>|<None>
    },
    "proxies": {
        "http": <str>,
        "https": <str>
    }
}
```

Here are the keys:

  * `subscription_type`: this object represents an OWM API Plan subscription. Possible values are: `free|startup|developer|professional|enterprise`
  * `language`: 2-char string representing the language you want the weather statuses returned in. Currently serving: `en|ru|ar|zh_cn|ja|es|it|fr|de|pt` and more. Check [here](https://openweathermap.org/current) for a comprehensive list of supported languages
  * `connection`:
    * `use_ssl`: whether to use SSL or not for API calls
    * `verify_ssl_certs`: speaks by itself..
    * `use_proxy`: whether to use a proxy server or not (useful if you're eg. in a corporate network). HTTP and SOCKS5 proxies are allowed
    * `timeout_secs`: after how many seconds the API calls should be timeouted
    * `max_retries`: how many times PyOWM should retry to call the API if it responds with an error or timeouts. Defaults to `None`, which means: call forever.
  * `proxies` (this sub-dict is ignored if `use_proxy == False`)
    * `http`: the HTTP URL of the proxy server
    * `https`: the HTTPS/SOCKS5 URL of the proxy server

## Providing a custom configuration
You can either pass in your custom dict to the global `OWM` object upon instantiation:

```python
from pyowm import OWM
owm = OWM('my-api-key', config=my_custom_config_dict)  # pass in your dict as a named argument
```

or you can put your custom configuration inside a JSON text file and have it read by PyOWM:

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_config_from
config_dict = get_config_from('/path/to/configfile.json')  # This utility comes in handy
owm = OWM('your-free-api-key', config_dict)
```

Be aware that the JSON file must be properly formatted and that the unspecified non-mandatory keys will be filled in with default values. Here is an example:

```json
{
    "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "subscription_type": "professional",
    "language": "ru",
    "connection": {
        "use_ssl": true,
        "verify_ssl_certs": true,
        "timeout_secs": 1
    }
}
```