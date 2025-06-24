import os
import time
from io import BytesIO
from typing import Optional
from urllib.error import HTTPError
from urllib.request import urlopen

import filetype  # type: ignore
import validators  # type: ignore
from bs4 import BeautifulSoup
from halo import Halo  # type: ignore
from mutagen.id3 import APIC, ID3, TALB, TIT2, TPE1
from mutagen.mp3 import MP3, HeaderNotFoundError
from PIL import Image as PILImage
from pydub import AudioSegment  # type: ignore
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from simple_chalk import chalk  # type: ignore

import beatstarsdownloader.url_helpers as helpers


class BeatStarsDownloader:
    def __init__(self, url: str, output_dir: str):
        self.url = url
        self.soup = self._get_soup(url)
        self.artist_name = self._get_artist_name(self.soup)
        self.dir_path = f"{output_dir}/{self.artist_name}"
        self.artwork: list[str] = []
        self.track_names: list[str] = []
        self.mp3_urls: list[str] = []

    def _scroll_down(self, driver: webdriver.Remote) -> None:
        """
        Selenium method to scroll down to end of page to ensure page is loaded.

        :param driver: webdriver
            Selenium web driver
        """
        # Get scroll height.
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load the page.
            time.sleep(3)
            # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _get_soup(self, url: str) -> BeautifulSoup:
        """
        Returns soup object of page if valid BeatStars url.

        :param url: str
            BeatStars URL for artist page.
        :return: BeautifulSoup
            Soup object of page
        """
        if not validators.url(url):
            url = "https://www.beatstars.com/" + url + "/tracks"
        if not helpers.is_bs_url(url):
            print(chalk.red.bold("✖ Doesn't look like a beatstars.com url..."))
            raise Exception()
        # print(url)
        with Halo(
            text=chalk.white.bold("Starting Selenium Webdriver..."), spinner="dots"
        ) as h:
            options = Options()
            options.add_argument("--headless")
            # options = webdriver.FirefoxOptions()
            # options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get(url)
            self._scroll_down(driver)
            page_source = driver.page_source
            driver.quit()
            h.stop_and_persist(
                symbol=f'{chalk.green("✔")}',
                text=chalk.green.dim("Selenium page loaded..."),
            )
        soup = BeautifulSoup(page_source, "html.parser")
        title_element = soup.find("span", {"class": "title"})
        if title_element:
            if title_element.text == "404":
                print(chalk.red.bold(f"✖ The url {url} returns 404..."))
                raise Exception(f"The url {url} returns 404...")
        return soup

    @staticmethod
    def _get_artist_name(soup: BeautifulSoup) -> str:
        """
        Returns artist name from BeatStars artist page soup object.

        :param soup: BeautifulSoup
            soup object of artist page on BeatStars
        :return: str
            artist name
        """
        name_element = soup.find("span", {"class": "name ng-star-inserted"})
        if name_element is None:
            raise ValueError("Artist name not found")
        return helpers.slugify(name_element.text.strip())

    def _get_tracks(self) -> None:
        """
        Returns BeatStars object of given BeatStars profile.

        :return:
            Returns a BeatStars Object
        """
        for track in self.soup.find_all(
            "mp-card-figure-template", {"class": "track-template"}
        ):
            track_object = track.find(  # type: ignore
                "a", {"class": "name ng-star-inserted"}  # type: ignore
            )
            if (
                track_object
                and hasattr(track_object, "text")
                and hasattr(track_object, "get")
            ):
                self.track_names.append(helpers.slugify(track_object.text.strip()))
                href = track_object.get("href")  # type: ignore
                if href:
                    self.mp3_urls.append(
                        f"https://main.v2.beatstars.com/stream?id="
                        f"{href.lstrip('/TK')}"
                        f"&return=audio"
                    )
                img_tag = track.find("img")  # type: ignore
                if img_tag:
                    src = img_tag.get("src")  # type: ignore
                    if src:
                        self.artwork.append(src)
            # print(self.mp3_urls)
            # print(self.artwork)

    def download_tracks(self, overwrite: bool, album: Optional[str] = None) -> None:
        # get a list of tracks with names, artwork urls and mp3 urls
        self._get_tracks()

        # make dir if not exists
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

        # use stub and mp3_urls to find all mp3 files on AWS and download them
        # avoid stop stealing beats page by adding in origin and referer to
        # request headers
        length_of_mp3_urls = len(self.mp3_urls)
        print(chalk.white.bold("-" * 10))
        print(
            chalk.white.bold(
                f"Downloading {length_of_mp3_urls} tracks by {self.artist_name}:"
            )
        )

        for i in range(len(self.mp3_urls)):
            num = i + 1
            with Halo(
                text=chalk.magenta(
                    f"Downloading track {num} of {length_of_mp3_urls}: "
                    f"{self.track_names[i]}..."
                ),
                spinner="dots",
            ) as halo:
                path = f"{self.dir_path}/{self.track_names[i]}.mp3"
                if os.path.exists(path) and not overwrite:
                    halo.stop_and_persist(
                        symbol=str(f'{chalk.yellow("〰")}'),
                        text=chalk.yellow.dim(
                            f"{num} • {path} already exists, skipping..."
                        ),
                    )
                    continue
                content = helpers.test_urls([self.mp3_urls[i]])
                if content:
                    try:
                        mp3 = MP3(BytesIO(content))
                    except HTTPError as e:
                        halo.stop_and_persist(
                            symbol=str(f'{chalk.red("✖")}'),
                            text=chalk.red.dim(f"HTTP ERROR: {e}"),
                        )
                    except HeaderNotFoundError as e:
                        # check to see if this is an audio file
                        mime = filetype.guess_mime(content).split("/")[0]
                        if mime == "audio":
                            mp3 = MP3(
                                AudioSegment.from_file(BytesIO(content)).export(
                                    format="mp3"
                                )
                            )
                        else:
                            halo.stop_and_persist(
                                symbol=str(f'{chalk.red("✖")}'),
                                text=chalk.red.dim(
                                    f"Mutagen ERROR: {e} " f"URL: {self.mp3_urls[i]}"
                                ),
                            )
                            continue
                    if mp3.tags is None:
                        mp3.tags = ID3()  # type: ignore
                    # ID3 Frames:
                    # https://mutagen.readthedocs.io/en/latest/api
                    # /id3_frames.html
                    # #id3v2-3-4-frames
                    if mp3.tags is not None:
                        mp3.tags["TPE1"] = TPE1(encoding=3, text=self.artist_name)
                        mp3.tags["TIT2"] = TIT2(encoding=3, text=self.track_names[i])
                    try:
                        album_art = urlopen(self.artwork[i]).read()
                    except (ValueError, HTTPError):
                        album_art = helpers.try_artwork(self.artwork, i)
                    # Convert image to PNG for compatibility
                    pil_img = PILImage.open(BytesIO(album_art))
                    img_byte_arr = BytesIO()
                    pil_img.save(img_byte_arr, format="PNG")
                    if mp3.tags is not None:
                        mp3.tags["APIC"] = APIC(
                            encoding=3,
                            mime="image/jpeg",
                            type=3,
                            desc="Cover",
                            data=img_byte_arr.getvalue(),
                        )
                    if album and mp3.tags is not None:
                        mp3.tags["TALB"] = TALB(encoding=3, text=album)
                    # Save mp3 then save metadata
                    with open(path, "wb") as f:
                        f.write(content)
                    mp3.save(path)
                    halo.stop_and_persist(
                        symbol=f'{chalk.green("✔")}',
                        text=chalk.green.dim(
                            f"{num} Saved "
                            f"{chalk.white.bold(self.track_names[i])} "
                            f"{chalk.green.dim(path)}"
                        ),
                    )
                else:
                    halo.stop_and_persist(
                        symbol=str(f'{chalk.red("✖")}'),
                        text=chalk.red.dim(
                            f"{num} BeatStars error skipping " f"{self.track_names[i]}"
                        ),
                    )
                    continue
