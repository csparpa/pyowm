"""
JSON test OWM API responses
"""

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

NO2INDEX_JSON_DUMP = '{"reference_time": 1234567, "no2_samples": [{"label": ' \
                    '"no2", "value": 8.168363052618588e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"label": "no2_strat", ' \
                    '"value": 8.686949115599418e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"label": "no2_trop", ' \
                    '"value": 8.871462853221601e-08, "precision": ' \
                    '-4.999999987376214e-07}], "location": {"country": "UK", ' \
                    '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                    '"ID": 987}, "interval": "day", "reception_time": 1475283600}'

SO2INDEX_JSON_DUMP = '{"reference_time": 1234567, "so2_samples": [{"pressure": ' \
                    '1000, "value": 8.168363052618588e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"pressure": 681.2920532226562, ' \
                    '"value": 8.686949115599418e-08, "precision": ' \
                    '-4.999999987376214e-07}, {"pressure": 464.15887451171875, ' \
                    '"value": 8.871462853221601e-08, "precision": ' \
                    '-4.999999987376214e-07}], "location": {"country": "UK", ' \
                    '"name": "test", "coordinates": {"lat": 43.7, "lon": 12.3}, ' \
                    '"ID": 987}, "interval": "day", "reception_time": 1475283600}'
