
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


class ImageTypeEnum:
    """
    Allowed image types on OWM APIs

    """
    PNG = ImageType('PNG', 'image/png')
    GEOTIFF = ImageType('GEOTIFF', 'image/tiff')

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
