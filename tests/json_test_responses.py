#!/usr/bin/env python

"""JSON test OWM API responses"""

OBSERVATION_JSON = '{"coord":{"lon":-0.12574,"lat":51.50853},"sys":{"country":' \
    '"GB","sunrise":1378877413,"sunset":1378923812},"weather":[{"id":804,' \
    '"main":"Clouds","description":"overcast clouds","icon":"04d"}],"base":' \
    '"gdps stations","main":{"temp":288.44,"pressure":1022,"temp_min":287.59,' \
    '"temp_max":289.82,"humidity":75},"wind":{"speed":1.54,"gust":2.57,"deg":' \
    '31},"clouds":{"all":92},"dt":1378895177,"id":2643743,"name":"London","cod":200}'
    
THREE_HOURS_FORECAST_JSON = '{"cod": "200","message": 0.0122,"city": {"id": 2643743,' \
    '"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},"country": ' \
    '"GB","population": 1000000},"cnt": 1,"list": [{"dt": 1378890000,"main":' \
    ' {"temp": 288.43,"temp_min": 286.968,"temp_max": 288.43,"pressure": 1026.07' \
    ',"sea_level": 1034.73,"grnd_level": 1026.07,"humidity": 75,"temp_kf": 1.46},' \
    '"weather": [{"id": 804,"main": "Clouds","description": "overcast clouds",' \
    '"icon": "04d"}],"clouds": {"all": 92},"wind": {"speed": 4.26,"deg": ' \
    '341.001},"sys": {"pod": "d"},"dt_txt": "2013-09-11 09:00:00"}]}'

DAILY_FORECAST_JSON = '{"cod": "200","message": 0.1019,"city": {"id": ' \
    '2643743,"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},' \
    '"country": "GB","population": 1000000},"cnt": 1\,"list": [{"dt": ' \
    '1378897200,"temp": {"day": 289.37,"min": 284.88,"max": 289.37,"night": ' \
    '284.88,"eve": 287.53,"morn": 289.37},"pressure": 1025.35,"humidity": 71,' \
    '"weather": [{"id": 500,"main": "Rain","description": "light rain","icon"' \
    ': "10d"}],"speed": 3.76,"deg": 338,"clouds": 48,"rain": 3}]}'

NOT_FOUND_JSON = '{"message":"Error: Not found city","cod":"404"}'