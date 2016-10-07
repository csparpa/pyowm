"""
JSON dumps for PyOWM test objects
"""

LOCATION_JSON_DUMP = '{"country": "UK", "name": "London", "coordinates": ' \
        + '{"lat": 43.7, "lon": 12.3}, "ID": 1234}'

WEATHER_JSON_DUMP = '{"status": "Clouds", "visibility_distance": 1000, ' \
                    '"clouds": 67, "temperature": {"temp_kf": -1.899, ' \
                    '"temp_min": 294.199, "temp": 294.199, "temp_max": 296.098},' \
                    ' "dewpoint": 300.0, "humidex": 298.0, "detailed_status": ' \
                    '"Overcast clouds", "reference_time": 1378459200, ' \
                    '"weather_code": 804, "sunset_time": 1378496400, "rain": ' \
                    '{"all": 20}, "snow": {"all": 0}, "pressure": ' \
                    '{"press": 1030.119, "sea_level": 1038.589}, ' \
                    '"sunrise_time": 1378449600, "heat_index": 40.0, ' \
                    '"weather_icon_name": "04d", "humidity": 57, "wind": ' \
                    '{"speed": 1.1, "deg": 252.002}}'

OBSERVATION_JSON_DUMP = '{"reception_time": 1234567, "Location": ' \
                        '{"country": "UK", "name": "test", "coordinates": ' \
                        '{"lat": 43.7, "lon": 12.3}, "ID": 987}, "Weather": ' \
                        '{"status": "Clouds", "visibility_distance": 1000, ' \
                        '"humidity": 57, "clouds": 67, "temperature": ' \
                        '{"temp_kf": -1.899, "temp_max": 296.098, ' \
                        '"temp": 294.199, "temp_min": 294.199}, ' \
                        '"dewpoint": 300.0, "snow": {"all": 0}, ' \
                        '"detailed_status": "Overcast clouds", ' \
                        '"reference_time": 1378459200, "weather_code": 804, ' \
                        '"humidex": 298.0, "rain": {"all": 20}, ' \
                        '"sunset_time": 1378496400, "pressure": ' \
                        '{"press": 1030.119, "sea_level": 1038.589}, ' \
                        '"sunrise_time": 1378449600, "heat_index": 296.0, ' \
                        '"weather_icon_name": "04d", "wind": ' \
                        '{"speed": 1.1, "deg": 252.002}}}'

FORECAST_JSON_DUMP = '{"reception_time": 1234567, "interval": "daily", ' \
                     '"Location": {"country": "IT", "name": "test", ' \
                     '"coordinates": {"lat": 43.7, "lon": 12.3}, "ID": 987}, ' \
                     '"weathers": [{"status": "Clouds", ' \
                     '"visibility_distance": 1000, "humidity": 57, "clouds": 67,' \
                     ' "temperature": {"temp_kf": -1.899, "temp_max": 296.098, ' \
                     '"temp": 294.199, "temp_min": 294.199}, "dewpoint": 300.0,' \
                     ' "snow": {"all": 0}, "detailed_status": "Overcast clouds",' \
                     ' "reference_time": 1378459200, "weather_code": 804, ' \
                     '"humidex": 298.0, "rain": {"all": 20}, ' \
                     '"sunset_time": 1378496400, "pressure": {"press": 1030.119,' \
                     ' "sea_level": 1038.589}, "sunrise_time": 1378449600, ' \
                     '"heat_index": 296.0, "weather_icon_name": "04d", "wind": ' \
                     '{"speed": 1.1, "deg": 252.002}}, {"status": "Clear", ' \
                     '"visibility_distance": 1000, "humidity": 12, ' \
                     '"clouds": 23, "temperature": {"temp_kf": -1.899, ' \
                     '"temp_max": 299.0, "temp": 297.199, "temp_min": 295.6}, ' \
                     '"dewpoint": 300.0, "snow": {"all": 0}, "detailed_status": ' \
                     '"Sky is clear", "reference_time": 1378459690, ' \
                     '"weather_code": 804, "humidex": 298.0, "rain": {"all": 10},' \
                     ' "sunset_time": 1378496480, "pressure": ' \
                     '{"press": 1070.119, "sea_level": 1078.589}, ' \
                     '"sunrise_time": 1378449510, "heat_index": 296.0, ' \
                     '"weather_icon_name": "02d", "wind": {"speed": 4.2, ' \
                     '"deg": 103.4}}]}'

STATIONHISTORY_JSON_DUMP = '{"reception_time": 1378684800, "interval": ' \
        + '"tick", "measurements": {"1362934043": {"wind": 4.7, "pressure": ' \
        + '1010.09, "temperature": 266.85, "rain": null, "humidity": 27.7}, ' \
        + '"1362933983": {"wind": 4.7, "pressure": 1010.02, "temperature": ' \
        + '266.25, "rain": null, "humidity": 27.3}}, "station_ID": 2865}'

STATION_JSON_DUMP = '{"status": 50, "distance": 18.95, "weather": {"status": ' \
                    '"Clouds", "visibility_distance": 1000, "humidity": 57, ' \
                    '"clouds": 67, "temperature": {"temp_kf": -1.899, ' \
                    '"temp_max": 296.098, "temp": 294.199, "temp_min": 294.199},' \
                    ' "dewpoint": 300.0, "snow": {"all": 0}, "detailed_status": ' \
                    '"Overcast clouds", "reference_time": 1378459200, ' \
                    '"weather_code": 804, "humidex": 298.0, "rain": {"all": 20},' \
                    ' "sunset_time": 1378496400, "pressure": ' \
                    '{"press": 1030.119, "sea_level": 1038.589}, ' \
                    '"sunrise_time": 1378449600, "heat_index": 296.0, ' \
                    '"weather_icon_name": "04d", "wind": {"speed": 1.1, ' \
                    '"deg": 252.002}}, "name": "KNGU", "station_type": 1, ' \
                    '"lat": 36.9375, "lon": -76.2893, "station_ID": 2865}'

UVINDEX_JSON_DUMP = '{"reference_time": 1234567, "location": {"country": "UK", ' \
                   '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                   '"ID": 987}, "interval": "day", "value": 6.8, ' \
                    '"reception_time": 1475283600}'

COINDEX_JSON_DUMP = '{"reference_time": 1234567, "co_samples": [{"pressure": ' \
                    '1000, "value": 8.168363052618588e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"pressure": 681.2920532226562, ' \
                    '"value": 8.686949115599418e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"pressure": 464.15887451171875, ' \
                    '"value": 8.871462853221601e-08, "precision": ' \
                    '-4.999999987376214e-07}], "location": {"country": "UK", ' \
                    '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                    '"ID": 987}, "interval": "day", "reception_time": 1475283600}'

OZONE_JSON_DUMP = '{"reference_time": 1234567, "location": {"country": "UK", ' \
                   '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                   '"ID": 987}, "interval": "day", "value": 6.8, ' \
                    '"reception_time": 1475283600}'