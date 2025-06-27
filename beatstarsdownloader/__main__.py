import argparse
import datetime
import os
import sys
from pathlib import Path
from typing import Optional

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import beatstarsdownloader.url_helpers as helpers
from beatstarsdownloader.beatstarsdownloader import BeatStarsDownloader
from beatstarsdownloader.config import __title__, __version__

console = Console()

# Unified questionary style for consistent formatting
QUESTIONARY_STYLE = questionary.Style(
    [
        ("question", "bold fg:#00aaaa"),
        ("pointer", "fg:#00aaaa bold"),
        ("highlighted", "fg:#00aaaa bold"),
        ("selected", "fg:#00aa00 bold"),
        ("checkbox", "fg:#00aaaa bold"),
        ("checkbox-selected", "fg:#00aa00 bold"),
        ("answer", "fg:#00aa00 bold"),
    ]
)


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def show_welcome_screen() -> None:
    """Display a styled welcome screen."""
    clear_screen()

    title_text = Text(__title__, style="bold blue")
    version_text = Text(f"Version: {__version__}", style="dim")
    copyright_text = Text(f"Copyright {datetime.datetime.now().year}", style="dim")

    welcome_content = Text()
    welcome_content.append(title_text)
    welcome_content.append("\n")
    welcome_content.append(version_text)
    welcome_content.append("\n")
    welcome_content.append(copyright_text)

    # Calculate the width based on the longest line in the ASCII art plus padding
    logo_lines = __title__.strip().split("\n")
    max_logo_width = max(len(line) for line in logo_lines if line.strip())
    panel_width = max_logo_width + 12  # Add more padding around the logo

    panel = Panel(
        welcome_content,
        title="BeatStars Downloader",
        border_style="blue",
        padding=(1, 2),
        width=panel_width,
    )
    console.print(panel)


def show_main_menu() -> bool:
    """Show main menu and return True to continue, False to exit."""
    choice = questionary.select(
        "What would you like to do?",
        choices=["Download an artist's tracks", "Exit program"],
        style=QUESTIONARY_STYLE,
    ).ask()

    if choice is None:
        return False
    return bool(choice == "Download an artist's tracks")


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
        show_welcome_screen()

        if not show_main_menu():
            console.print("\n[yellow]Goodbye![/yellow]")
            sys.exit(0)

        console.print("\n[bold green]Let's get started![/bold green]")

        url = questionary.text(
            "Enter the URL or name of the artist you want to scrape:",
            style=QUESTIONARY_STYLE,
        ).ask()

        default_dir = str(Path.home()) + "/beatstarsdownloader"
        output_dir = questionary.text(
            f"Output directory (default: {default_dir}):",
            default=default_dir,
            style=QUESTIONARY_STYLE,
        ).ask()

        overwrite = questionary.confirm(
            "Overwrite files if they already exist?",
            default=False,
            style=QUESTIONARY_STYLE,
        ).ask()

        album = (
            questionary.text(
                "Album ID3 tag (for music library sorting, leave blank to skip):",
                default="",
                style=QUESTIONARY_STYLE,
            ).ask()
            or None
        )

        track_select = questionary.confirm(
            "Do you want to select specific tracks to download?",
            default=False,
            style=QUESTIONARY_STYLE,
        ).ask()

        return output_dir, album, overwrite, url, track_select


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
