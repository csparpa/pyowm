from django.core.exceptions import ValidationError


def validate_longitude(lon):
    if lon < -180.0 or lon > 180.0:
        raise ValidationError("Longitude value must be between -180 and 180")


def validate_latitude(lat):
    if lat < -90.0 or lat > 90.0:
        raise ValidationError("Latitude value must be between -90 and 90")
