import setuptools
from beatstarsdownloader import __version__

with open("README.md", "r")as f:
    long_description = f.read()

setuptools.setup(
    name="beatstarsdownloader",
    packages=['beatstarsdownloader'],
    version=__version__,
    description="CLI for downloading BeatStars tracks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tim Morriss",
    url="https://github.com/tim-morriss/beatstarsdownloader",
    download_url="https://github.com/tim-morriss/beatstarsdownloader/archive/refs/tags/v0.1.0.tar.gz",
    license="MIT",
    keywords=['beatstars', 'downloader'],
    install_requires=[
        'beautifulsoup4',
        'filetype',
        'halo',
        'mutagen',
        'pick',
        'pillow',
        'pydub',
        'requests',
        'selenium>=4.16.0',
        'setuptools',
        'simple-chalk',
        'tqdm',
        'validators',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'beatstarsdownloader = beatstarsdownloader.__main__:run'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13'
    ]
)
