# TMDB-Trakt-Syncer

This Python script syncs user watchlist and ratings for Movies, TV Shows, and Episodes both ways between [Trakt](https://trakt.tv/) and [TMDB](https://www.themoviedb.org/). Data already set will not be overwritten. Ratings are synced by default and watchlist sync is optional. The user will be prompted to enter their preferences and api keys on first run. 

The script is compatible on any operating system that supports Python v3.6 or later, including Windows, Linux, Mac, and ChromeOS. If you're interested in syncing ratings between Trakt, Plex, IMDB, and TMDB, I recommend the following projects: [PlexTraktSync](https://github.com/Taxel/PlexTraktSync), [IMDB-Trakt-Syncer](https://github.com/RileyXX/IMDB-Trakt-Syncer), and [TMDB-Trakt-Syncer](https://github.com/RileyXX/TMDB-Trakt-Syncer).

## Installation Instructions:
1. Install [Python](https://www.python.org/downloads/) (v3.6 or later).
2. Install the script by running `python -m pip install TMDBTraktSyncer` in command line.
3. Login to [Trakt](https://trakt.tv/oauth/applications) and create a new API application named `TMDbTraktSyncer`. In the "Redirect uri" field, enter `urn:ietf:wg:oauth:2.0:oob`, then save the application.
4. Login to [TMDB](https://www.themoviedb.org/settings/api/) and create a new API application. Choose "Developer" and accept the terms. Fill out the application form as follows: 
   - Type of use: `Personal`
   - Application name: `TMDB-Trakt-Sync`
   - Application URL: `localhost`
   - Application summary: `Use TMDB API and Trakt API to sync user ratings between platforms. https://github.com/RileyXX/TMDB-Trakt-Syncer`
   - Fill in the rest of the fields as desired and submit the form. Your API keys will be generated instantly.
5. Run the script by running `TMDBTraktSyncer` in the command line.
6. Follow the prompts during the first run. You will need to enter your Trakt client ID and client secret from step 3, as well as your `tmdb_v4_token` from step 4. Please note that these details are saved insecurely as `credentials.txt` in the same folder as the script.
7. Setup is complete. The script will continue running and syncing your ratings. You can monitor its progress in the command line.

## Installing the Script:
```
python -m pip install TMDBTraktSyncer
```
_Run in your operating system's native command line._
## Running the Script:
```
TMDBTraktSyncer
```
_Run in your operating system's native command line._
## Updating the Script:
```
python -m pip install TMDBTraktSyncer --upgrade
```
_Run in your operating system's native command line._
## Uninstalling the Script:
```
python -m pip uninstall TMDBTraktSyncer
```
_Run in your operating system's native command line._

## Installing a Specific Version:
```
python -m pip install TMDBTraktSyncer==VERSION_NUMBER
```
_Replace `VERSION_NUMBER` with your [desired version](https://github.com/RileyXX/TMDB-Trakt-Syncer/releases) (e.g. 1.0.1) and run in your operating system's native command line._

## Alternative Manual Installation Method (without pip install):
1. Install [Python](https://www.python.org/downloads/) (v3.6 or later).
2. Download the latest .zip from the [releases page](https://github.com/RileyXX/TMDB-Trakt-Syncer/releases) and extract it to the desired directory.
3. Login to [Trakt](https://trakt.tv/oauth/applications) and create a new API application named `TMDBTraktSyncer`. In the "Redirect uri" field, enter `urn:ietf:wg:oauth:2.0:oob`, then save the application.
4. Login to [TMDB](https://www.themoviedb.org/settings/api/) and create a new API application. Choose "Developer" and accept the terms. Fill out the application form as follows: 
   - Type of use: `Personal`
   - Application name: `TMDB-Trakt-Sync`
   - Application URL: `localhost`
   - Application summary: `Use TMDB API and Trakt API to sync user ratings between platforms. https://github.com/RileyXX/TMDB-Trakt-Syncer`
   - Fill in the rest of the fields as desired and submit the form. Your API keys will be generated instantly.
5. Run `TMDBTraktSyncer.py` or open the terminal and navigate to the folder where `TMDBTraktSyncer.py` is located, then run `TMDBTraktSyncer.py` in the terminal.
6. Follow the prompts during the first run. You will need to enter your Trakt client ID and client secret from step 3, as well as your `tmdb_v4_token` from step 4. Please note that these details are saved insecurely as `credentials.txt` in the same folder as the script.
7. Setup is complete. The script will continue running and syncing your ratings. You can monitor its progress in the command line.

## For Setting Up Automation See the Following Wiki Pages:
- Setup Automation for:
   - [Windows](https://github.com/RileyXX/TMDB-Trakt-Syncer/wiki/Setting-Up-Automation-on-Windows)
   - [Linux](https://github.com/RileyXX/TMDB-Trakt-Syncer/wiki/Setting-Up-Automation-on-Linux)
   - [macOS](https://github.com/RileyXX/TMDB-Trakt-Syncer/wiki/Setting-Up-Automation-on-macOS)
- Python Script to Update all Packages with Pip (Windows, Linux, Mac, ChromeOS, etc.) [Link #1](https://github.com/RileyXX/TMDB-Trakt-Syncer/wiki/Python-Script-to-Update-all-Packages-with-Pip-\(Windows,-Linux,-Mac,-ChromeOS,-etc\))

## Troubleshooting, Known Issues, Workarounds & Future Outlook:
* Add support for review/comment sync [Issue #1](https://github.com/RileyXX/TMDB-Trakt-Syncer/issues/1)
* If any of your details change (passwords, logins, API keys, etc.), simply open `credentials.txt`, modify your details, save it and then run the script again. Alternatively, delete `credentials.txt` to reset the script and it will prompt you to enter your new details on the next run.

## Screenshot:
![Demo](https://i.imgur.com/5LI04O2.png)

## Sponsorships, Donations, and Custom Projects:
If you find my scripts helpful, you can become a [sponsor](https://github.com/sponsors/RileyXX) and support my projects! If you need help with a project, open an issue, and I'll do my best to assist you. For other inquiries and custom projects, you can contact me on [Twitter](https://twitter.com/RileyxBell).

#### More Donation Options:
- Cashapp: `$rileyxx`
- Venmo: `@rileyxx`
- Bitcoin: `bc1qrjevwqv49z8y77len3azqfghxrjmrjvhy5zqau`
- Amazon Wishlist: [Link ↗](https://www.amazon.com/hz/wishlist/ls/WURF5NWZ843U)

## Also Posted on:
* [PyPi](https://pypi.org/project/TMDBTraktSyncer/)
* [Reddit](https://www.reddit.com/r/trakt/comments/13jlu4r/tmdb_trakt_rating_syncer_tool_2_way_sync/)

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
