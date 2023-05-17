# TMDB-Trakt-Syncer
This python script will sync user ratings for Movies and TV Shows both ways between Trakt and TMDB. Ratings already set will not be overwritten. This script should work on an OS where python is supported (Windows, Linux, Mac, ChromeOS, etc). If you're looking to sync your ratings between Trakt, Plex, IMDB, and TMDB then these are my recommended projects: [PlexTraktSync](https://github.com/Taxel/PlexTraktSync), [IMDb-Trakt-Syncer](https://github.com/RileyXX/IMDb-Trakt-Syncer) & [TMDB-Trakt-Syncer](https://github.com/RileyXX/TMDB-Trakt-Syncer).
## Install Instructions:
1. Install [Python](https://www.python.org/downloads/). 
2. Run `python -m pip install TMDBTraktSyncer` in command line.
3. Login to [Trakt](https://trakt.tv/oauth/applications) and create a new API application. We will name it `TMDbTraktSyncer`. In the Redirect uri field enter `urn:ietf:wg:oauth:2.0:oob` then Save. 
4. Login to [TMDB](https://www.themoviedb.org/settings/api/) and create a new API application. Choose developer, accept the terms and start filling out the application form. For type of use `Personal`. For application name we will call it `TMDB-Trakt-Sync`. For application url enter `localhost`. For application summary enter `Use TMDB api and Trakt api to sync user ratings between platforms. https://github.com/RileyXX/TMDB-Trakt-Syncer`. Fill in the rest of the fields with whatever you want and submit. Your api keys will be instantly generated.
5. Run the script by calling `TMDBTraktSyncer` in command line. 
6. Follow the prompts on first run. It will ask you to fill in your Trakt client id and client secret from step 3. It will also ask you to fill in your tmdb_v4_token from step 4. Please note that these details are saved insecurely as credentials.txt in the same folder as the script.
7. Done, setup complete. The script will continue to run and sync your ratings. This may take some time, you can follow its progress in the command line.

## Run:
`TMDBTraktSyncer` in command line.

## Update:
`python -m pip install TMDBTraktSyncer --upgrade` in command line.

## Uninstall:
`python -m pip uninstall TMDBTraktSyncer` in command line.

## Install specific version:
`python -m pip install TMDBTraktSyncer==VERSION_NUMBER` in command line. Replace `VERSION_NUMBER` with your [desired version](https://github.com/RileyXX/TMDb-Trakt-Syncer/releases).

## Alternative manual no pip install method:
1. Install [Python](https://www.python.org/downloads/).
2. Download the latest .zip from the [releases page](https://github.com/RileyXX/TMDB-Trakt-Syncer/releases) and extract it to the file directory of your choice.
3. Login to [Trakt](https://trakt.tv/oauth/applications) and create a new API application. We will name it `TMDBTraktSyncer`. In the Redirect uri field enter `urn:ietf:wg:oauth:2.0:oob` then Save. 
4. Login to [TMDB](https://www.themoviedb.org/settings/api/) and create a new API application. Choose developer, accept the terms and start filling out the application form. For type of use `Personal`. For application name we will call it `TMDB-Trakt-Sync`. For application url enter `localhost`. For application summary enter `Use TMDB api and Trakt api to sync user ratings between platforms. https://github.com/RileyXX/TMDB-Trakt-Syncer`. Fill in the rest of the fields with whatever you want and submit. Your api keys will be instantly generated.
5. Run `TMDBTraktSyncer.py` OR open terminal and navigate to folder where `TMDBTraktSyncer.py` is located. Run `TMDBTraktSyncer.py` in terminal. 
6. Follow the prompts on first run. It will ask you to fill in your Trakt client id and client secret from step 3. It will also ask you to fill in your tmdb_v4_token from step 4. Please note that these details are saved insecurely as credentials.txt in the same folder as the script. 
7. Done. The script will continue to run and sync your ratings. This may take some time, you can follow its progress in the command line.

## Troubleshooting, known issues, workarounds & future outlook:
* Add support for review/comment sync https://github.com/RileyXX/TMDB-Trakt-Syncer/issues/1
* If any of your details change, passwords, logins, api keys etc, just delete credentials.txt and that will reset the script. It will prompt you to enter your new details on next run.

## Screenshot:
![Demo](https://i.imgur.com/5LI04O2.png)


## Sponsorships, Donations and Custom Projects:
Like my scripts? Become a [sponsor](https://github.com/sponsors/RileyXX) and support my projects! See below for other donation options. Need help with a project? Open an issue and I will try my best to help! For other inquiries and custom projects contact me on [Twitter](https://twitter.com/RileyxBell).

#### More donation options:
- Cashapp: `$rileyxx`
- Venmo: `@rileyxx`
- Bitcoin: `bc1qrjevwqv49z8y77len3azqfghxrjmrjvhy5zqau`
- Amazon Wishlist: [Link ↗](https://www.amazon.com/hz/wishlist/ls/WURF5NWZ843U)

## Also posted on:
* [PyPi](https://pypi.org/project/TMDBTraktSyncer/)
* [Reddit](https://www.reddit.com/r/trakt/comments/13jlu4r/tmdb_trakt_rating_syncer_tool_2_way_sync/)

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
