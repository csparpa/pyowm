def obfuscate_API_key(API_key):
    """
    Return a mostly obfuscated version of the API Key

    :param API_key: input string
    :return: str
    """
    if API_key is not None:
        return (len(API_key)-8)*'*'+API_key[-8:]
