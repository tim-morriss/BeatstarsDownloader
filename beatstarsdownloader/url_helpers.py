import os
import re
import unicodedata
from simple_chalk import chalk
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def is_local(url: str):
    """
    Parse url and check if it is a local file or a web url

    :param url:
        str: url to parse
    :return: bool
    """
    url_parsed = urlparse(url)
    if url_parsed.scheme in ('file', ''):  # Possibly a local file
        return os.path.exists(url_parsed.path)
    return False


def slugify(value: str, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils
    /text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii',
                                                            'ignore').decode(
            'ascii')
    # value = re.sub(r'[^\w\s-]', '', value.lower())
    value = re.sub(r'[^\w\s-]', '', value)
    return re.sub(r'[-\s]+', ' ', value).strip('-_')


def test_urls(urls: list):
    """
    Test TrakTrain url to see if it raises HTTPError or not.
    Note: some tracks are not available from the AWS server,
    this is an issue with Traktrain.

    :param urls:
        list: list of urls to test
    :return:
        urlopen object
    """
    for url in reversed(urls):
        try:
            return urlopen(Request(url)).read()
        except HTTPError as e:
            continue


def try_artwork(artwork: list, index: int):
    """
    Try artwork sizes to see if they can be accessed successfully.

    :param artwork:
        list: Artwork to test
    :return:
        urlopen object
    """
    for art in (artwork[index:] + artwork[:index]):
        try:
            return urlopen(art).read()
        except (ValueError, HTTPError):
            continue


def is_bs_url(bs_url: str):
    """
    Check to see if url starts with beatstars.com

    :param bs_url:
        string: url to test
    :return:
        bool: True if it is a BeatStars url, else False
    """
    if type(bs_url) is not str:
        print(chalk.red.bold("Doesn't look like you provided a URL..."))
        exit()
    if bs_url.startswith("https://beatstars.com/"):
        return True
    elif bs_url.startswith("https://www.beatstars.com/"):
        return True
    else:
        return False
