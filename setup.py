import setuptools

from beatstarsdownloader import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="beatstarsdownloader",
    packages=["beatstarsdownloader"],
    version=__version__,
    description="Tool for downloading all BeatStars tracks from an artist to mp3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Morriss",
    url="https://github.com/tim-morriss/BeatstarsDownloader",
    download_url=(
        "https://github.com/tim-morriss/BeatstarsDownloader/"
        "archive/refs/tags/v0.1.2.tar.gz"
    ),
    license="MIT",
    keywords=["beatstars", "downloader", "mp3", "music"],
    install_requires=[
        "beautifulsoup4>=4.13.4,<5.0.0",
        "filetype>=1.2.0,<2.0.0",
        "halo>=0.0.31,<0.0.32",
        "mutagen>=1.47.0,<2.0.0",
        "pick>=2.4.0,<3.0.0",
        "pillow>=11.2.1,<12.0.0",
        "pydub>=0.25.1,<0.26.0",
        "requests>=2.32.4,<3.0.0",
        "selenium>=4.33.0,<5.0.0",
        "simple-chalk>=0.1.0,<0.2.0",
        "tqdm>=4.67.1,<5.0.0",
        "validators>=0.35.0,<0.36.0",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": ["beatstarsdownloader = beatstarsdownloader.__main__:run"]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
