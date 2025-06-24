# BeatStarsDownloader

Python script for downloading all tracks from a beatstars artist track page. 
It functions as a BeatStars downloader to mp3.

Fork from [pyscrapetrain](https://github.com/tim-morriss/pyscrapeTrain).

# Setup
There are two ways to run this tool, either using the pip package or manually installing the tool.

Pip package method is preferred, only resort to using the manual install if you're having issues.
## Pip Package

Install the pip package, using this command:

```bash
pip install beatstarsdownloader
```

## Manual install
First clone this repo, then install dependencies using Poetry:

```bash
poetry install
```

Then run the tool using this command:

```bash
poetry run python main.py
```

*For the rest of the readme, make sure to swap out the `beatstarsdownloader` command for `poetry run python main.py`.*

# How to use:
## Terminal interface
Feel free to use the built in terminal interface to download tracks from a single URL / artist name:

```bash
beatstarsdownloader
```
![image](https://raw.githubusercontent.com/tim-morriss/beatstarsdownloader/main/media/terminal_ui.png)


## CLI interface

**When inputting a url make sure to use the artist's /tracks page.**

**For example: `https://www.beatstars.com/lovbug/tracks`**

----

To download all the tracks from a profile run the following command:

```bash
beatstarsdownloader <beatstars tracks url or artist name>
```

For example: 
```bash
beatstarsdownloader https://www.beatstars.com/lovbug/tracks
```
OR
```bash
beatstarsdownloader lovbug
```

Tracks are downloaded to a `beatstarsDownloader/artist` folder in your home directory. 
## Changing folder
To change download folder use the `-d` flag:
```bash
beatstarsdownloader <beatstars-url> -d /path/to/folder
```

Which will create a `beatstarsDownloader/artist` folder under the path specified.
For example:
```bash
beatstarsdownloader https://www.beatstars.com/lovbug/tracks -d /Users/user/Documents
```
Will create the following folder `/Users/user/Documents/beatstarsDownloader/lovbug`.

## Adding custom album
You might want to listen to the playlist of tracks you just downloaded 
so the script supports a custom album ID3 tag to allow you to sort in your media library.

Use the `-a` tag to assign a custom album name.

For example:
```bash
beatstarsdownloader https://www.beatstars.com/lovbug/tracks -a "bs lovbug"
```

Which gives:
![image](https://raw.githubusercontent.com/tim-morriss/beatstarsdownloader/main/media/album_example.png)

## Supplying a list of URLs

If you want to scrape multiple beatstars pages then you can point a .txt file 
with each url you want to scrape on a new line.

For this use-case simply specify the filepath instead of a url.

For example:
```bash
beatstarsdownloader example_url_list.txt
```

Example list of urls:
![image](https://raw.githubusercontent.com/tim-morriss/beatstarsdownloader/main/media/example_url_list.png)

# Disclaimer

**THIS TOOL IS STRICTLY FOR EDUCATIONAL PURPOSES ONLY.**

**THE AUTHOR TAKES NO RESPONSIBILITY FOR THE USAGE OF THIS TOOL.**

Disclaimer: Use of BeatstarsDownloader (this tool)

This tool, BeatstarsDownloader, is provided to you as a convenience of downloading web assets. Before using this tool, it is important to understand and acknowledge the following:

**Copyrighted Material**: The Author (referring to the author of this code) does not endorse or encourage the unauthorized downloading or distribution of copyrighted music. This tool is intended for use with music that you have the legal right to download and distribute.

**User Responsibility**: The user acknowledges and agrees that they are solely responsible for ensuring that their use of BeatstarsDownloader complies with applicable copyright laws and regulations. Users must obtain the necessary permissions or licenses before downloading and using copyrighted material.

**Legal Compliance**: The Author is not responsible for any legal consequences that may arise from the use of this tool for downloading copyrighted music without the proper authorization. Users should be aware of and comply with the copyright laws in their jurisdiction.

**No Warranty**: The Author provides this tool "as is" without any warranty of any kind, expressed or implied. The Author makes no representations or warranties regarding the accuracy, reliability, or completeness of the tool.

**Updates and Changes**: The Author reserves the right to make changes or updates to this tool at any time without notice. It is the user's responsibility to ensure they are using the latest version of the tool.

By using BeatstarsDownloader, you agree to the terms and conditions outlined in this disclaimer. If you do not agree with these terms, you should not use the tool.
