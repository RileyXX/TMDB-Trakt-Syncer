from setuptools import setup, find_packages
import codecs
import os

#To create package: python setup.py sdist bdist_wheel
#To upload package: twine upload dist/*

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.7'
DESCRIPTION = 'This python script syncs user watchlist and ratings for Movies, TV Shows and Episodes both ways between Trakt and TMDB.'

# Setting up
setup(
    name="TMDBTraktSyncer",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/RileyXX/TMDB-Trakt-Syncer",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'video', 'trakt', 'tmdb', 'ratings', 'sync', 'movies', 'tv shows'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'TMDBTraktSyncer = TMDBTraktSyncer.TMDBTraktSyncer:main'
        ]
    },
    python_requires='>=3.6'
)