
class MapLayerEnum:
    """
    Allowed map layer values for tiles retrieval

    """
    PRECIPITATION = 'precipitation_new'
    WIND = 'wind_new'
    TEMPERATURE = 'temp_new'
    PRESSURE = 'pressure_new'

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            cls.PRECIPITATION,
            cls.WIND,
            cls.TEMPERATURE,
            cls.PRESSURE
        ]
