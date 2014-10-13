#!/usr/bin/env python

"""JSON test OWM API responses"""

OBSERVATION_JSON = '{"coord":{"lon":-0.12574,"lat":51.50853},"sys":{"country":' \
    '"GB","sunrise":1378877413,"sunset":1378923812},"weather":[{"id":804,' \
    '"main":"Clouds","description":"overcast clouds","icon":"04d"}],"base":' \
    '"gdps stations","main":{"temp":288.44,"pressure":1022,"temp_min":287.59,' \
    '"temp_max":289.82,"humidity":75},"wind":{"speed":1.54,"gust":2.57,"deg":' \
    '31},"clouds":{"all":92},"dt":1378895177,"id":2643743,"name":"London","cod":200}'

SEARCH_RESULTS_JSON = '{"cod": "200", "count": 2, "list": [{"clouds": {"all": ' \
    '20}, "coord": {"lat": 51.50853, "lon": -0.12573999999999999}, "dt": 1378237178,' \
    ' "id": 2643743, "main": {"humidity": 56, "pressure": 1025, "temp": ' \
    '293.74000000000001, "temp_max": 296.14999999999998, "temp_min": ' \
    '291.48000000000002}, "name": "London", "sys": {"country": "GB"}, "weather": ' \
    '[{"description": "fewclouds", "icon": "02n", "id": 801, "main": "Clouds"}], ' \
    '"wind": {"deg": 0, "speed": 1}}, {"clouds": {"all": 20}, "coord": {"lat": ' \
    '45.50853, "lon": 2.567}, "dt": 1378237178, "id": 2943743, "main": {"humidity": ' \
    '56, "pressure": 1025, "temp": 293.74000000000001, "temp_max": ' \
    '296.14999999999998, "temp_min": 291.48000000000002}, "name": "Wonderland", ' \
    '"sys": {"country": "GB"}, "weather": [{"description": "fewclouds", "icon": ' \
    '"02n", "id": 801, "main": "Clouds"}], "wind": {"deg": 0, "speed": 1}}]}'

THREE_HOURS_FORECAST_JSON = '{"cod": "200","message": 0.0122,"city": {"id": 2643743,' \
    '"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},"country": ' \
    '"GB","population": 1000000},"cnt": 1,"list": [{"dt": 1378890000,"main":' \
    ' {"temp": 288.43,"temp_min": 286.968,"temp_max": 288.43,"pressure": 1026.07' \
    ',"sea_level": 1034.73,"grnd_level": 1026.07,"humidity": 75,"temp_kf": 1.46},' \
    '"weather": [{"id": 804,"main": "Clouds","description": "overcast clouds",' \
    '"icon": "04d"}],"clouds": {"all": 92},"wind": {"speed": 4.26,"deg": ' \
    '341.001},"sys": {"pod": "d"},"dt_txt": "2013-09-11 09:00:00"}]}'

THREE_HOURS_FORECAST_AT_COORDS_JSON = '{"cod": "200","message": 0.0982,"city": ' \
    '{"id": 6690989,"name": "Bethnal Green","coord": {"lon": -0.06109,"lat": ' \
    '51.52718},"country": "GB","population": 0},"cnt": 25,"list": [{"dt": ' \
    '1413104400,"main": {"temp": 283.77,"temp_min": 282.26,"temp_max": 283.77,' \
    '"pressure": 1016.84,"sea_level": 1027.17,"grnd_level": 1016.84,' \
    '"humidity": 94,"temp_kf": 1.51},"weather": [{"id": 803,"main": "Clouds",' \
    '"description": "broken clouds","icon": "04d"}],"clouds": {"all": 76},' \
    '"wind": {"speed": 2.85,"deg": 59.0039},"rain": {"3h": 0},"sys": {"pod": ' \
    '"d"},"dt_txt": "2014-10-12 09:00:00"}]}' 

DAILY_FORECAST_JSON = '{"cod": "200","message": 0.1019,"city": {"id": ' \
    '2643743,"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},' \
    '"country": "GB","population": 1000000},"cnt": 1,"list": [{"dt": ' \
    '1378897200,"temp": {"day": 289.37,"min": 284.88,"max": 289.37,"night": ' \
    '284.88,"eve": 287.53,"morn": 289.37},"pressure": 1025.35,"humidity": 71,' \
    '"weather": [{"id": 500,"main": "Rain","description": "light rain","icon"' \
    ': "10d"}],"speed": 3.76,"deg": 338,"clouds": 48,"rain": 3}]}'

DAILY_FORECAST_AT_COORDS_JSON = '{"cod": "200","message": 0.0038,"city": ' \
    '{"id": 6690574,"name": "Clerkenwell","coord": {"lon": -0.11022,"lat": ' \
    '51.52438},"country": "GB","population": 0},"cnt": 7,"list": [{"dt": ' \
    '1413111600,"temp": {"day": 286.25,"min": 282.63,"max": 286.54,"night": ' \
    '284.54,"eve": 285.51,"morn": 282.63},"pressure": 1016.13,"humidity": 91,' \
    '"weather": [{"id": 501,"main": "Rain","description": "moderate rain",' \
    '"icon": "10d"}],"speed": 2.85,"deg": 66,"clouds": 76,"rain": 4}]}'

CITY_WEATHER_HISTORY_JSON = '{"message": "","cod": "200","city_id": 2643743,' \
    '"calctime": 0.5363,"cnt": 1,"list": [{"weather": [{"id": 500,"main": "Rain"' \
    ',"description": "light rain","icon": "10d"}],"base": "gdps stations","main":' \
    ' {"temp": 290.31,"pressure": 1011,"humidity": 82,"temp_min": 288.15,"temp_max"' \
    ': 292.59},"wind": {"speed": 3.6,"deg": 160},"rain": {"1h": 0.25},"clouds": ' \
    '{"all": 40},"city": {"zoom": 13,"country": "GB","population": 1000000,"find":' \
    ' ["LONDON"],"id": 2643743,"name": "London"},"dt": 1378459300},' \
    '{"weather": [{"id": 500,"main": "Rain"' \
    ',"description": "rain","icon": "10d"}],"base": "gdps stations","main":' \
    ' {"temp": 288.31,"pressure": 1015,"humidity": 87,"temp_min": 284.15,"temp_max"' \
    ': 292.59},"wind": {"speed": 3.6,"deg": 160},"rain": {"1h": 0.75},"clouds": ' \
    '{"all": 70},"city": {"zoom": 13,"country": "GB","population": 1000000,"find":' \
    ' ["LONDON"],"id": 2643743,"name": "London"},"dt": 1378498200}]}'

OBSERVATION_NOT_FOUND_JSON = '{"message":"Error: Not found city","cod":"404"}'

INTERNAL_SERVER_ERROR_JSON = '{"message":"Error: Internal server error","cod":"500"}'

SEARCH_WITH_NO_RESULTS_JSON = '{"cod": "200", "count": 0, "list": []}'

FORECAST_NOT_FOUND_JSON = '{"cod": "200","message": 0.0122,"city": {"id": 2643743,' \
    '"name": "London","coord": {"lon": -0.12574,"lat": 51.50853},"country": ' \
    '"GB","population": 1000000},"cnt": 0,"list": []}'

CITY_WEATHER_HISTORY_NOT_FOUND_JSON = '{"message":"no data","cod":"404"}'

CITY_WEATHER_HISTORY_NO_RESULTS_JSON = '{"calctime" : 1.9337,"city_id" : 4219762,' \
    '"cnt" : 0,"cod" : "200","list" : [],"message" : ""}'

STATION_TICK_WEATHER_HISTORY_JSON = '{"message": "", "cod": "200", "type": "tick", ' \
    '"station_id": 39276, "calctime": "tick=0.0128total=1.1367", "cnt": 30, ' \
    '"list": [{"temp": 266.25, "main": {"temp": 266.25, "humidity": 27.1, ' \
    '"pressure": 1010.03}, "humidity": 27.1, "pressure": 1010.03, "dt": 1362933923},' \
    ' {"temp": 266.25, "main": {"temp": 266.25, "humidity": 27.3, "pressure": ' \
    '1010.02}, "humidity": 27.3, "pressure": 1010.02, "dt": 1362933983}]}'

STATION_WEATHER_HISTORY_JSON = '{"message": "", "cod": "200", "type": "hour", ' \
    '"station_id": 35579, "calctime": 0.1122, "cnt": 1, "list": [{"temp": {"v": ' \
    '281.48, "c": 2, "mi": 281.48, "ma": 281.48}, "pressure": {"v": 1024, "c": 2,' \
    ' "mi": 1024, "ma": 1024}, "humidity": {"v": 98, "c": 2, "mi": 98, "ma": 98},' \
    ' "rain": {"today": {"v": 19.81, "c": 2, "mi": 19.812, "ma": 19.812}}, "wind":' \
    ' {"speed": {"v": 4.37, "c": 2, "mi": 4.11, "ma": 4.63}, "deg": {"v": 356}}, ' \
    '"main": {"humidity": {"v": 98, "c": 2, "mi": 98, "ma": 98}, "temp": {"v": 281.48,' \
    ' "c": 2, "mi": 281.48, "ma": 281.48}, "temp_max": 281.48, "pressure": {"v": 1024,' \
    ' "c": 2, "mi": 1024, "ma": 1024}}, "dt": 1381140000}]}'

STATION_WEATHER_HISTORY_NOT_FOUND_JSON = '{"message":"","cod":"200","type":"tick",' \
    '"station_id":11347,"calctime":" tick = 0.1258 total=1.7684","cnt":0,"list":[]}'
