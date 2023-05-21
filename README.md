# TMDB-Trakt-Syncer

This Python script syncs user ratings for Movies, TV Shows, and Episodes both ways between [Trakt](https://trakt.tv/) and [TMDB](https://www.themoviedb.org/). Ratings already set will not be overwritten. The script is compatible on any operating system that supports Python v3.6 or later, including Windows, Linux, Mac, and ChromeOS. If you're interested in syncing ratings between Trakt, Plex, IMDB, and TMDB, I recommend the following projects: [PlexTraktSync](https://github.com/Taxel/PlexTraktSync), [IMDB-Trakt-Syncer](https://github.com/RileyXX/IMDB-Trakt-Syncer), and [TMDB-Trakt-Syncer](https://github.com/RileyXX/TMDB-Trakt-Syncer).

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

## For Setting Up Automation See the Following Sections:
- Python Script to Update all Packages with Pip (Windows, Linux, Mac, ChromeOS, etc. [Link #1](https://github.com/RileyXX/TMDB-Trakt-Syncer/blob/main/README.md#python-script-to-update-all-packages-with-pip-windows-linux-mac-chromeos-etc)
- Windows: Creating a .bat File to Run Multiple Python Projects and Optional Steps for Opening Programs and Creating a Shortcut to Run On Demand From Desktop. [Link #2](https://github.com/RileyXX/TMDB-Trakt-Syncer/blob/main/README.md#windows-creating-a-bat-file-to-run-multiple-python-projects-and-optional-steps-for-opening-programs-and-creating-a-shortcut-to-run-on-demand-from-desktop)
- Windows: Auto-Running a File on Login, Once per Day, or Hourly using Task Scheduler (Background Execution. [Link #3](https://github.com/RileyXX/TMDB-Trakt-Syncer/blob/main/README.md#windows-auto-running-a-file-on-login-once-per-day-or-hourly-using-task-scheduler-background-execution)

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

## Python Script to Update all Packages with Pip (Windows, Linux, Mac, ChromeOS, etc)
1. Create a new .txt file and rename it to `AutoUpdatePythonPackages.py`
2. Open `AutoUpdatePythonPackages.py` file in a text editor, copy the following code and save it to the `.py` file.
```python
import subprocess

ignored_packages = ['chromedriver-py']  # Add or remove which python packages/projects you would like to ignore from auto-updates e.g. ['Project 1', 'Project 2', 'Project 3'] or no packages with []

subprocess.call(['pip', 'install', '--upgrade', 'pip'])

# Get a list of outdated packages
outdated_packages = subprocess.check_output(['pip', 'list', '--outdated']).decode().split('\n')

# Update each outdated package (excluding chromedriver-py)
for package in outdated_packages:
    if package:
        package_name = package.split(' ')[0]
        if package_name not in ignored_packages:
            subprocess.call(['pip', 'install', '-U', package_name])

if not outdated_packages:
    print("All packages are up to date.")
```
3. Run the file.
4. (Optional) Edit the `ignored_packages` value to exclude packages and projects from auto-updating.
5. (Optional) For automation on Windows, including auto-running a file on login, once per day, or hourly. See this [section](https://github.com/RileyXX/TMDB-Trakt-Syncer/edit/main/README.md#windows-auto-running-a-file-on-login-once-per-day-or-hourly-using-task-scheduler-background-execution).

## Windows: Creating a .bat File to Run Multiple Python Projects and Optional Steps for Opening Programs and Creating a Shortcut to Run On Demand From Desktop

This guide will walk you through the steps to create a .bat file that can run multiple Python projects installed with path variables. Additionally, it includes optional steps for opening multiple programs and creating a shortcut with an icon for easy on-demand execution from the desktop.

### Prerequisites

Before you begin, ensure the following:

- Python is installed on your system.
- The Python projects you want to run are installed and added to the system's PATH environment variable. Projects installed with pip are typically already added to the system's PATH environment variable.

### Steps

1. Open a text editor and create a new file called `run_projects.bat`.

2. Add the following lines to the file:

```batch
@echo off

python -m project1

python -m project2

python -m project3

```

   Replace `project1`, `project2`, and `project3` with the actual names of your Python projects. You can add as many lines as needed for each project.

3. Save the file with a `.bat` extension, for example, `run_projects.bat`.

4. (Optional) Steps to Open Multiple Programs:

   If you want to open multiple programs (e.g. Plex Media Server), add the following lines to the `.bat` file.

   ```batch
   start "" "C:\path\to\program1.exe"

   start "" "C:\path\to\program2.exe"

   start "" "C:\path\to\program3.exe"
   ```

   Replace `program1.exe`, `program2.exe`, and `program3.exe` with the actual paths to the programs you want to open. You can add as many lines as needed for each program.

5. (Optional) Creating a Shortcut with an Icon:

   To create a shortcut with an icon for easy on-demand execution from the desktop, follow these steps:

   - Right-click on the desktop and select "New" > "Shortcut".
   - In the "Create Shortcut" dialog, click "Browse" and navigate to the location of the `.bat` file.
   - Click "Next".
   - Provide a name for the shortcut, for example, "Run Projects".
   - Click "Finish".
   - Right-click on the newly created shortcut and select "Properties".
   - In the "Properties" dialog, click "Change Icon" and browse to select an icon file of your choice.
   - Click "OK" to save the changes.

6. Run the .bat File:

   - Double-click the `.bat` file or shortcut you created to execute it. This will run the specified Python projects (and open programs if included) in the order specified.

7. (Optional) Run the Shortcut:

   - Double-click the shortcut you created on the desktop to execute the `.bat` file and run the Python projects (and open programs if included).

That's it! You have successfully created a `.bat` file to run multiple Python projects, optionally opening multiple programs before execution, and optionally created a shortcut with an icon for easy on-demand execution from the desktop.

## Windows: Auto-Running a File on Login, Once per Day, or Hourly using Task Scheduler (Background Execution)

This guide will walk you through the steps to configure Windows Task Scheduler to automatically run any file on login, once per day, or hourly, ensuring it runs in the background without displaying a prompt window.

### Steps

1. Place the File:
   - Place the file you want to run in a specific location on your computer. For example, you can create a folder called "AutoRun" in your user directory and place a filed called "AutoRun.bat" inside it.

2. Open Task Scheduler:
   - Press `Win + R` to open the "Run" dialog box.
   - Type `taskschd.msc` and press Enter. This will open the Task Scheduler.

3. Create a New Task:
   - In the Task Scheduler window, click on "Create Task" in the right-hand pane.

4. Configure the Task:
   - Provide a name and description for the task (e.g., "AutoRunFile").
   - Choose "Run whether the user is logged on or not" for executing in the background without a prompt window. Or choose "Run only when user is logged on" to display the prompt window.
   - Select "Trigger" and choose "At log on" for login-based execution.
     - (Optional) For hourly execution as part of "At log on":
       - Click "New" under "Actions".
       - Set the action as follows:
         - Action: Start a program
         - Program/script: Browse and select the file you want to run. Provide the full path to the file if it is located outside the system's PATH environment variable.
         - Start in: Provide the full path to the folder containing the file.
       - Click "OK" to save the action.
       - Set the desired "Delay task for" time to specify the interval between log on and executing the task.
   - (Optional) For once-per-day execution:
     - Select "Trigger" and choose "Daily".
     - Set the frequency to "1" and select the desired time of day to run the task.
   - Select the appropriate user account for which the task should run.
   - Under "Actions", click "New" and set the action as follows:
     - Action: Start a program
     - Program/script: Browse and select the file you want to run. Provide the full path to the file if it is located outside the system's PATH environment variable.
     - Add arguments (if necessary): Specify any additional arguments or parameters required by the file.
     - Start in: Provide the full path to the folder containing the file.
   - Configure any additional settings as needed (e.g., conditions, settings, etc.).
   - Click "OK" to save the task.

5. Test the Auto-Startup and Background Execution:
   - Select the task you created and click Run in the right side panel to test the setup.
   - Restart your computer to test the setup for login-based execution.
   - Alternatively, wait for the scheduled time to test the setup for once-per-day or hourly execution.
   - After login or at the scheduled time, the specified file should run in the background without displaying a prompt window. You can verify this by checking if the file executes as expected.

That's it! You have successfully set up Windows Task Scheduler to auto-run any file on login, once per day, or hourly as part of the "At log on" trigger, ensuring it runs in the background without a prompt window.
