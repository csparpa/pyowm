import sys


def obfuscate_API_key(API_key):
    """
    Return a mostly obfuscated version of the API Key

    :param API_key: input string
    :return: str
    """
    if API_key is not None:
        return (len(API_key)-8)*'*'+API_key[-8:]


def check_if_running_with_python_2():
    """
    Catch Python 2.x usage attempts. If Python2
    :return: `None`
    :raise: `ImportError` if running on Python 2
    """
    if sys.version_info < (3,):
        raise ImportError(
            """You are running PyOWM on Python 2 - how unfortunate! Since version 2.10, 
PyOWM does not support Python 2 any more. PyOWM 2.9 has however a Long-Term Support
branch for bug fixing on Python 2 - install it with:

 $ pip install git+https://github.com/csparpa/pyowm.git@v2.9-LTS

This LTS branch will be maintained until January, 1 2020

See details at:

https://github.com/csparpa/pyowm/wiki/Timeline-for-dropping-Python-2.x-support

""")
