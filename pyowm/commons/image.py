
class Image:

    """
    Wrapper class for a generic image
    :param data: raw image data
    :type data: bytes
    :param mime_type: the MIME type of the image, if known
    :type mime_type: str or `None`
    """

    def __init__(self, data, mime_type=None):
        self.data = data
        self.mime_type = mime_type

    def persist(self, path_to_file):
        with open(path_to_file, 'wb') as f:
            f.write(self.data)

    @classmethod
    def load(kls, path_to_file):
        import mimetypes
        mimetypes.init()
        mime = mimetypes.guess_type('file://%s' % path_to_file)[0]
        with open(path_to_file, 'rb') as f:
            data = f.read()
        return Image(data, mime_type=mime)
