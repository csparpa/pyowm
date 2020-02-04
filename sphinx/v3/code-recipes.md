# Code recipes

This section provides code snippets you can use to quickly get started with PyOWM when performing common enquiries
related to weather data.

Table of contents:
  * [Library initialization](#library_init)
  * [Weather data](#weather_data)

<div id="library_init"/>

## Library initialization

### 1. Initialize PyOWM with default configuration and a free API key
```python
from pyowm.owm import OWM
owm = OWM('your-free-api-key')
```

### 2. Initialize PyOWM with configuration loaded from an external JSON file
You can setup a configuration file and then have PyOWM read it. The file must contain a valid JSON document with the
following format:

```
{
    "subscription_type": free|startup|developer|professional|enterprise
    "language": en|ru|ar|zh_cn|ja|es|it|fr|de|pt|... (check https://openweathermap.org/current) 
    "connection": {
        "use_ssl": true|false,
        "verify_ssl_certs": true|false,
        "use_proxy": true|false,
        "timeout_secs": N
    },
    "proxies": {
        "http": HTTP_URL,
        "https": SOCKS5_URL
    }
}
```

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_config_from
config_dict = get_config_from('/path/to/configfile.json')
owm = OWM('your-free-api-key', config_dict)
```

### 3. Initialize PyOWM with a paid subscription - eg: professional
If you bought a paid subscription then you need to provide PyOWM both your paid API key and the subscription type that you've bought

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config_for_subscription_type
config_dict = get_default_config_for_subscription_type('professional')
owm = OWM('your-paid-api-key', config_dict)
```

### 4. Use PyOWM behind a proxy server
If you have an HTTP or SOCKS5 proxy server you need to provide PyOWM two URLs; one for each HTTP and HTTPS protocols.
URLs are in the form: 'protocol://username:password@proxy_hostname:proxy_port'

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config_for_proxy
config_dict = get_default_config_for_proxy(
    'http://user:pass@192.168.1.77:8464',
    'https://user:pass@192.168.1.77:8934'
)
owm = OWM('your-api-key', config_dict)
```

### 5. Language setting
English is the default - but you can change it
Check out [https://openweathermap.org/current](https://openweathermap.org/current) for the complete list of supported languages

```python
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'pt'  # your language here
owm = OWM('your-api-key', config_dict)
```

### 6. Get PyOWM configuration
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
config_dict = owm.configuration
```

### 7. Get the version of PyOWM library
```python
from pyowm.owm import OWM
owm = OWM('your-api-key')
version_tuple = (major, minor, patch) = owm.version
```

<div id="weather_data"/>

## Weather data
TBD
