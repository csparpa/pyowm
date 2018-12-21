"""
URIs templates for resources exposed by the Agro API 1.0
"""

ROOT_AGRO_API = 'http://api.agromonitoring.com/agro/1.0'

# Polygons API subset
POLYGONS_URI = ROOT_AGRO_API + '/polygons'
NAMED_POLYGON_URI = ROOT_AGRO_API + '/polygons/%s'

# Soil API subset
SOIL_URI = ROOT_AGRO_API + '/soil'

# Satellite Imagery Search API subset
SATELLITE_IMAGERY_SEARCH_URI = ROOT_AGRO_API + '/image/search'
