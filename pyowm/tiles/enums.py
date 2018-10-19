class MapLayerEnum:
    """
    Allowed map layer values for tiles retrieval

    """
    PRECIPITATION = 'precipitation_new'
    WIND = 'wind_new'
    TEMPERATURE = 'temperature_new'
    PRESSURE = 'pressure_new'

    def items(self):
        """
        All values for this enum
        :return: list of tuples

        """
        return [
            ('PRECIPITATION', self.PRECIPITATION),
            ('WIND', self.WIND),
            ('TEMPERATURE', self.TEMPERATURE),
            ('PRESSURE', self.PRESSURE)
        ]
