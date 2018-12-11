from pyowm.commons.databoxes import ImageType


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
    def lookup_by_name(cls, name):
        for i in ImageTypeEnum.items():
            if i.name == name:
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
