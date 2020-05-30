from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# ---------- FREE API KEY ---------------------

owm = OWM('your-API-key')  # You MUST provide a valid API key

# Search for current weather in London (Great Britain)
mgr = owm.weather_manager()
observation = mgr.weather_at_place('London,GB')
w = observation.weather
print(w)                  # <Weather - reference time=2013-12-18 09:20, status=Clouds>

# Weather details
w.wind()                  # {'speed': 4.6, 'deg': 330}
w.humidity                # 87
w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

# Search current weather observations in the surroundings of
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
observation_list = mgr.weather_around_coords(-22.57, -43.12)


# ---------- PAID API KEY ---------------------

config_dict = config.get_default_config_for_subscription_type('professional')
owm = OWM('your-paid-api-key', config_dict)

# Will it be clear tomorrow at this time in Milan (Italy) ?
mgr = owm.weather_manager()
forecast = mgr.forecast_at_place('Milan,IT', 'daily')
forecast.will_be_clear_at(timestamps.tomorrow())  # The sun always shines on Italy, right? ;)
