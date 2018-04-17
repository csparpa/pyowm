def obfuscate_API_key(API_key):
    """
    Return a mostly obfuscated version of the API Key

    :param API_key: input string
    :return: str
    """
    if API_key is not None:
        return (len(API_key)-8)*'*'+API_key[-8:]


def assert_is_string(value):
    """
    Checks if the provided value is a valid string instance

    :param value: value to be checked
    :return: None
    """
    try:  # Python 2.x
        assert isinstance(value, basestring), "Value must be a string or unicode"
    except NameError:  # Python 3.x
        assert isinstance(value, str), "Value must be a string"


def assert_is_string_or_unicode(value):
    """
    Checks if the provided value is a valid string or unicode instance
    On Python 3.x it just checks that the value is a string instance.
    :param value: value to be checked
    :return: None
    """
    try:
        assert isinstance(value, basestring) or isinstance(value, unicode), \
            "Value must be a string or unicode"
    except NameError:
        assert isinstance(value, str), "Value must be a string"


def encode_to_utf8(value):
    """
    Turns the provided value to UTF-8 encoding

    :param value: input value
    :return: UTF-8 encoded value
    """
    try:  # The OWM API expects UTF-8 encoding
        if not isinstance(value, unicode):
            return value.encode('utf8')
        return value
    except NameError:
        return value