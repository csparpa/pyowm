
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

    @classmethod
    def lookup_by_mime_type(cls, mime_type):
        for i in ImageTypeEnum.items():
            if i.mime_type == mime_type:
                return i
        return None

    @classmethod
    def items(cls):
        """
        All values for this enum
        :return: list of `pyowm.commons.enums.ImageType`

        """
        return [
            cls.PNG,
            cls.GEOTIFF
        ]

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
