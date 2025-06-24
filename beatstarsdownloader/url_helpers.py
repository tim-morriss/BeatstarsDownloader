import os
import re
import unicodedata
from typing import Any, Optional
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from simple_chalk import chalk  # type: ignore


def is_local(url: str) -> bool:
    """
    Parse url and check if it is a local file or a web url

    :param url:
        str: url to parse
    :return: bool
    """
    url_parsed = urlparse(url)
    if url_parsed.scheme in ("file", ""):  # Possibly a local file
        return os.path.exists(url_parsed.path)
    return False


def slugify(value: str, allow_unicode: bool = False) -> str:
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
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    # value = re.sub(r'[^\w\s-]', '', value.lower())
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", " ", value).strip("-_")


def test_urls(urls: list[str]) -> Optional[Any]:
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
            return urlopen(
                Request(url=url, headers={"User-Agent": "Mozilla/5.0"})
            ).read()
        except HTTPError:
            continue
    return None


def try_artwork(artwork: list, index: int) -> Optional[Any]:
    """
    Try artwork sizes to see if they can be accessed successfully.

    :param artwork:
        list: Artwork to test
        index: index of artwork to start with
    :return:
        urlopen object
    """
    for art in artwork[index:] + artwork[:index]:
        try:
            return urlopen(art).read()
        except (ValueError, HTTPError):
            continue
    return None


def is_bs_url(bs_url: str) -> bool:
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
