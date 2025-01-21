import os
import json
import sys
import datetime
from datetime import timedelta
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from TMDBTraktSyncer import authTrakt
from TMDBTraktSyncer import errorLogger as EL

def print_directory(main_directory):
    print(f"Your settings are saved at:\n{main_directory}")

def prompt_get_credentials():
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Default values to use if no credentials are provided
    default_values = {
        "trakt_client_id": "empty",
        "trakt_client_secret": "empty",
        "trakt_access_token": "empty",
        "trakt_refresh_token": "empty",
        "tmdb_access_token": "empty",
        "last_trakt_token_refresh": "empty"
    }

    # Check if the file exists and is not empty
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        # If the file does not exist or is empty, create it with default values
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(default_values, f, indent=4, separators=(', ', ': '))
    
    # Read the file only once and parse JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            values = json.load(f)
        except json.decoder.JSONDecodeError:
            # Handle the case where the file is empty or not a valid JSON
            values = default_values

    # Check for deprecated key and rename it if needed
    if "tmdb_v4_token" in values:
        values["tmdb_access_token"] = values.pop("tmdb_v4_token")

    # Add missing default values
    values = {**default_values, **values}

    # Prompt the user only for missing or empty values (except for tokens that can be refreshed)
    for key, value in values.items():
        if value == "empty" and key not in ["trakt_access_token", "trakt_refresh_token", "last_trakt_token_refresh"]:
            if key == "trakt_client_id":
                print("\n")
                print("***** TRAKT API SETUP *****")
                print("If this is your first time setting up, follow these instructions to setup your Trakt API application:")
                print("  1. Login to Trakt and navigate to your API apps page: https://trakt.tv/oauth/applications")
                print('  2. Create a new API application named "TMDBTraktSyncer".')
                print('  3. In the "Redirect uri" field, enter "urn:ietf:wg:oauth:2.0:oob", then save the application.')
                print("\n")
                values[key] = input("Please enter your Trakt Client ID: ").strip()
            elif key == "tmdb_access_token":
                print("\n")
                print("***** TMDB API SETUP *****")
                print("If this is your first time setting up, follow these instructions to setup your TMDB API application:")
                print("  1. Login to TMDB and navigate to your API apps page: https://www.themoviedb.org/settings/api/")
                print('  2. Create a new API application. Choose "Developer" and accept the terms.')
                print("  3. Fill out the application form as follows:")
                print('     - Type of use: Personal')
                print('     - Application name: TMDB-Trakt-Sync')
                print('     - Application URL: https://github.com/RileyXX/TMDB-Trakt-Syncer')
                print('     - Application summary: Use TMDB API and Trakt API to sync user watchlists and ratings between platforms.')
                print('     - Fill in the rest of the fields as desired and submit the form. Your API keys will be generated instantly.')
                print("\n")
                values[key] = input("Please enter your TMDB Access Token: ").strip()
            else:
                values[key] = input(f"Please enter a value for {key}: ").strip()

    # Update the file only if any values were changed
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(values, f, indent=4, separators=(', ', ': '))

    # Check if it's time to refresh the Trakt tokens (7 days interval)
    last_trakt_token_refresh = values.get("last_trakt_token_refresh", "empty")
    should_refresh = True
    if last_trakt_token_refresh != "empty":
        try:
            last_trakt_token_refresh_time = datetime.datetime.fromisoformat(last_trakt_token_refresh)
            if datetime.datetime.now() - last_trakt_token_refresh_time < timedelta(days=7):
                should_refresh = False
        except ValueError:
            pass

    # Refresh tokens if necessary
    if should_refresh:
        trakt_access_token = values.get("trakt_refresh_token", "empty")
        client_id = values["trakt_client_id"]
        client_secret = values["trakt_client_secret"]
        
        if trakt_access_token != "empty":
            trakt_access_token, trakt_refresh_token = authTrakt.authenticate(client_id, client_secret, trakt_access_token)
        else:
            trakt_access_token, trakt_refresh_token = authTrakt.authenticate(client_id, client_secret)

        # Update the values and last refresh timestamp
        values["trakt_access_token"] = trakt_access_token
        values["trakt_refresh_token"] = trakt_refresh_token
        values["last_trakt_token_refresh"] = datetime.datetime.now().isoformat()

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(values, f, indent=4, separators=(', ', ': '))

    # Return the required credentials
    return values["trakt_client_id"], values["trakt_client_secret"], values["trakt_access_token"], values["trakt_refresh_token"], values["tmdb_access_token"]
        
def prompt_sync_ratings():
    """
    Check or prompt the user to determine if ratings should be synced.

    Returns:
        bool: True if syncing ratings, False otherwise.
    """
    # Define the file path
    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'credentials.txt')

    # Attempt to read the existing value from the credentials file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
            sync_ratings_value = credentials.get('sync_ratings')
            if isinstance(sync_ratings_value, bool):
                return sync_ratings_value
    except FileNotFoundError:
        EL.logger.error("Credentials file not found.", exc_info=True)
        credentials = {}
    except json.JSONDecodeError:
        EL.logger.error("Error decoding credentials file.", exc_info=True)
        credentials = {}

    # Prompt the user for input if value is not found or invalid
    while True:
        user_input = input("Do you want to sync ratings? (y/n): ").strip().lower()
        if user_input in ('y', 'n'):
            sync_ratings_value = user_input == 'y'
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    # Save the updated value to the credentials file
    credentials['sync_ratings'] = sync_ratings_value
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(credentials, file, indent=4, separators=(', ', ': '))
    except Exception as e:
        EL.logger.error("Error writing to credentials file: %s", e, exc_info=True)

    return sync_ratings_value

def prompt_sync_watchlist():
    """
    Prompts the user to enable or disable watchlist syncing and stores the preference in a credentials file.
    Minimizes file reads and writes while handling errors gracefully.

    Returns:
        bool: The user's preference for syncing the watchlist.
    """
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Attempt to read the existing sync_watchlist value from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
            sync_watchlist_value = credentials.get('sync_watchlist')
            if sync_watchlist_value not in [None, "empty"]:
                return sync_watchlist_value
    except FileNotFoundError:
        EL.error("Credentials file not found. Proceeding to prompt user.", exc_info=True)
        credentials = {}
    except json.JSONDecodeError:
        EL.error("Invalid JSON format in credentials file. Proceeding to prompt user.", exc_info=True)
        credentials = {}

    # Prompt the user for input
    while True:
        user_input = input("Do you want to sync watchlists? (y/n): ").strip().lower()
        if user_input in {'y', 'n'}:
            sync_watchlist_value = (user_input == 'y')
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # Update the file with the new sync_watchlist value
    credentials['sync_watchlist'] = sync_watchlist_value
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(credentials, file, indent=4, separators=(', ', ': '))
    except Exception as e:
        EL.error("Failed to write to credentials file.", exc_info=True)

    return sync_watchlist_value

def prompt_remove_watched_from_watchlists():
    """
    Function to check or prompt the user for their preference on removing watched items 
    from watchlists. Minimizes file read/write operations and ensures clarity.
    """
    # Define the file path
    here = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(here, 'credentials.txt')

    # Load credentials from file (if it exists)
    credentials = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            credentials = json.load(file)
    except FileNotFoundError:
        EL.logger.error("Credentials file not found.", exc_info=True)

    # Check existing preference in credentials
    remove_watched_from_watchlists_value = credentials.get('remove_watched_from_watchlists')
    if remove_watched_from_watchlists_value is not None and remove_watched_from_watchlists_value != "empty":
        return remove_watched_from_watchlists_value

    # Prompt the user for input if preference is not set
    print("Movies and Episodes are removed from watchlists after 1 play.")
    print("Shows are removed when at least 80% of the episodes are watched AND the series is marked as ended or cancelled.")
    while True:
        user_input = input("Do you want to remove watched items from watchlists? (y/n): ").strip().lower()
        if user_input in ['y', 'n']:
            remove_watched_from_watchlists_value = (user_input == 'y')  # Convert to boolean
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # Update credentials and write back to file
    credentials['remove_watched_from_watchlists'] = remove_watched_from_watchlists_value
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(credentials, file, indent=4, separators=(', ', ': '))
    except IOError as e:
        EL.logger.error("Failed to write to credentials file.", exc_info=True)

    return remove_watched_from_watchlists_value