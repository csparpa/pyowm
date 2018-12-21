class ImageType:
    """
    Databox class representing an image type

    :param name: the image type name
    :type name: str
    :param mime_type: the image type MIME type
    :type mime_type: str
    """
    def __init__(self, name, mime_type):

        self.name = name
        self.mime_type = mime_type

    def __repr__(self):
        return "<%s.%s - name=%s mime=%s>" % (
            __name__, self.__class__.__name__, self.name, self.mime_type)


class Satellite:
    """
    Databox class representing a satellite

    :param name: the satellite
    :type name: str
    :param symbol: the short name of the satellite
    :type symbol: str
    """
    def __init__(self, name, symbol):

        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return "<%s.%s - name=%s symbol=%s>" % (
            __name__, self.__class__.__name__, self.name, self.symbol)

