import argparse
import datetime
import sys
from pathlib import Path
from typing import Optional

from pick import Picker  # type: ignore
from typing_extensions import override

import beatstarsdownloader.url_helpers as helpers
from beatstarsdownloader.beatstarsdownloader import BeatStarsDownloader
from beatstarsdownloader.config import __title__, __version__


class CustomPicker(Picker):
    def __init__(self, *args, **kwargs):  # type: ignore
        super().__init__(*args, **kwargs)

    @override
    def get_title_lines(self, max_width: int = 0) -> list[str]:
        if self.title:
            return self.title.split("\n") + [""]
        else:
            return []


def query_yes_no(question: str, default: str = "yes") -> bool:
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def cli() -> tuple[str, Optional[str], bool, str, Optional[bool]]:
    parser = argparse.ArgumentParser(
        description="Tool for downloading BeatStars tracks."
    )

    parser.add_argument(
        "url",
        nargs="?",
        default=None,
        type=str,
        help="url for the BeatStars profile",
    ),
    parser.add_argument(
        "-d",
        "--dir",
        dest="directory",
        default=None,
        type=str,
        help="directory to save mp3s to. format: <dir>/beatstarsdownloader/<artist>",
    )
    parser.add_argument(
        "-a",
        "--album",
        dest="album",
        default=None,
        type=str,
        help="Custom name for ID3 tags, for sorting",
    )
    parser.add_argument(
        "-o", "--overwrite", dest="overwrite", default=False, action="store_true"
    )
    parser.add_argument(
        "-t",
        "--track_select",
        dest="track_select",
        default=False,
        action="store_true",
        help="Allows you to interactively select tracks to download",
    )

    if sys.argv[1:]:
        args = parser.parse_args(args=sys.argv[1:])
        if not args.directory:
            # os agnostic home path
            output_dir = str(Path.home()) + "/beatstarsdownloader"
        else:
            output_dir = args.directory
        # define where to save mp3s
        album = args.album
        overwrite = args.overwrite
        url = args.url
        track_select = args.track_select
        return output_dir, album, overwrite, url, track_select
    else:
        first_menu_options = ["Download an artist's tracks", "Exit program"]
        first_menu_title = (
            rf"{__title__}"
            f"\n Version: {__version__}"
            f"\n Copyright {datetime.datetime.now().year}"
        )
        picker = CustomPicker(
            options=first_menu_options, title=first_menu_title, indicator=">"
        )
        _, first_menu_index = picker.start()
        if first_menu_index == 0:
            url = input("Enter the URL or name of the " "artist you want to scrape: ")
            output_dir = (
                input(
                    "What is the output directory you want to use "
                    "(leave blank for default): "
                )
                or str(Path.home()) + "/beatstarsdownloader"
            )
            overwrite = query_yes_no(
                "Overwrite files if they already exist?", default="no"
            )
            album = (
                input(
                    "Do you want to save the output with an album ID3 "
                    "tag (good for sorting in your music library, "
                    "leave blank to turn off): "
                )
                or None
            )
            track_select = query_yes_no(
                "BeatstarsDownloader can download all tracks by an artist or "
                "download specific tracks. Do you want to select the tracks "
                "to download?",
                default="no",
            )
            return output_dir, album, overwrite, url, track_select
        elif first_menu_index == 1:
            exit()
        else:
            raise ValueError("Invalid menu selection")


def run() -> None:
    output_dir, album, overwrite, url, track_select = cli()

    if helpers.is_local(url):
        try:
            if url.endswith(".txt"):
                with open(url) as f:
                    lines = f.readlines()
                    lines = list(set(lines))
                    for line in lines:
                        try:
                            BeatStarsDownloader(
                                line.strip(), output_dir
                            ).download_tracks(overwrite, album, track_select)
                        except Exception as e:
                            print(e)
            else:
                raise Exception("Please supply a txt file")
        except Exception as e:
            print(e)
    else:
        BeatStarsDownloader(url, output_dir).download_tracks(
            overwrite, album, track_select
        )
