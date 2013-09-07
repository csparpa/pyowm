__VERSION__ = 0.1
__OWM_API_VERSION__ = 2.5

#OpenWeatherMap API URLs
API_URL = 'http://api.openweathermap.org/data/2.5'
ICONS_BASE_URL = 'http://openweathermap.org/img/w'
OBSERVATION_URL = API_URL+'/weather'
FIND_OBSERVATIONS_URL = API_URL+'/find'
THREE_HOURS_FORECAST_URL = API_URL+'/forecast'
DAILY_FORECAST_URL = API_URL+'/forecast/daily'


#Submodules imports
from location import Location
from weather import Weather
from observation import Observation