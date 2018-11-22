from pyowm.commons.enums import ImageType, ImageTypeEnum


class Image:

    """
    Wrapper class for a generic image

    :param data: raw image data
    :type data: bytes
    :param image_type: the type of the image, if known
    :type image_type: `pyowm.commons.enums.ImageType` or `None`
    """

    def __init__(self, data, image_type=None):
        self.data = data
        if image_type is not None:
            assert isinstance(image_type, ImageType)
        self.image_type = image_type

    def persist(self, path_to_file):
        with open(path_to_file, 'wb') as f:
            f.write(self.data)

    @classmethod
    def load(kls, path_to_file):
        import mimetypes
        mimetypes.init()
        mime = mimetypes.guess_type('file://%s' % path_to_file)[0]
        img_type = ImageTypeEnum.lookup_by_mime_type(mime)
        with open(path_to_file, 'rb') as f:
            data = f.read()
        return Image(data, image_type=img_type)
