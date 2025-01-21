import os
import json
import requests
import time
import sys
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from TMDBTraktSyncer import arguments

def main():

    parser = argparse.ArgumentParser(description="TMDBTraktSyncer CLI")
    parser.add_argument("--clear-user-data", action="store_true", help="Clears user entered credentials.")
    parser.add_argument("--clear-cache", action="store_true", help="Clears error logs and other cached data.")
    parser.add_argument("--uninstall", action="store_true", help="Clears cached data except user entered credentials before uninstalling.")
    parser.add_argument("--clean-uninstall", action="store_true", help="Clears all cached data, inluding user credentials before uninstalling.")
    parser.add_argument("--directory", action="store_true", help="Prints the package install directory.")
    
    args = parser.parse_args()
    
    main_directory = os.path.dirname(os.path.realpath(__file__))

    if args.clear_user_data:
        arguments.clear_user_data(main_directory)
    
    if args.clear_cache:
        arguments.clear_cache(main_directory)
    
    if args.uninstall:
        arguments.uninstall(main_directory)
    
    if args.clean_uninstall:
        arguments.clean_uninstall(main_directory)
    
    if args.directory:
        arguments.print_directory(main_directory)
    
    # If no arguments are passed, run the main package logic
    if not any([args.clear_user_data, args.clear_cache, args.uninstall, args.clean_uninstall, args.directory]):
    
        # Run main package
        print("Starting TMDBTraktSyncer....")
        from TMDBTraktSyncer import checkVersion as CV
        from TMDBTraktSyncer import verifyCredentials as VC
        from TMDBTraktSyncer import traktData
        from TMDBTraktSyncer import tmdbData
        from TMDBTraktSyncer import errorHandling as EH
        from TMDBTraktSyncer import errorLogger as EL
    
        # Check if package is up to date
        CV.checkVersion()

        try:
            # Print credentials directory
            VC.print_directory(main_directory)
        
            # Save the credential values as variables
            _, _, _, _, _ = VC.prompt_get_credentials()
            sync_ratings_value = VC.prompt_sync_ratings()
            sync_watchlist_value = VC.prompt_sync_watchlist()
            remove_watched_from_watchlists_value = VC.prompt_remove_watched_from_watchlists()
            
            # Initalize list values
            trakt_watchlist = trakt_ratings = watched_content = tmdb_watchlist = tmdb_ratings = []
            
            print('Processing Trakt Data')
            trakt_encoded_username = traktData.get_trakt_encoded_username()
            if sync_watchlist_value or remove_watched_from_watchlists_value:
                trakt_watchlist = traktData.get_trakt_watchlist(trakt_encoded_username)
            if sync_ratings_value:
                trakt_ratings = traktData.get_trakt_ratings(trakt_encoded_username)
            if remove_watched_from_watchlists_value:
                watched_content = traktData.get_trakt_watch_history(trakt_encoded_username)
            print('Processing Trakt Data Complete')
            
            print('Processing TMDB Data')
            tmdb_account_id = tmdbData.fetch_account_id()
            if sync_watchlist_value or remove_watched_from_watchlists_value:
                tmdb_watchlist = tmdbData.get_tmdb_watchlist(tmdb_account_id)
            if sync_ratings_value:
                tmdb_ratings = tmdbData.get_tmdb_ratings(tmdb_account_id)
            print('Processing TMDB Data Complete')
            
            # Filter out items that share the same Title, Year and Type, AND have non-matching TMDB_IDs
            trakt_ratings, tmdb_ratings = EH.filter_mismatched_items(trakt_ratings, tmdb_ratings)
            trakt_watchlist, tmdb_watchlist = EH.filter_mismatched_items(trakt_watchlist, tmdb_watchlist)

            #Get trakt and tmdb ratings and filter out trakt ratings with missing tmdb id
            trakt_ratings = [rating for rating in trakt_ratings if rating['TMDB_ID'] is not None]
            tmdb_ratings = [rating for rating in tmdb_ratings if rating['TMDB_ID'] is not None]
            trakt_watchlist = [item for item in trakt_watchlist if item['TMDB_ID'] is not None]
            tmdb_watchlist = [item for item in tmdb_watchlist if item['TMDB_ID'] is not None]
            #Filter out ratings already set
            tmdb_ratings_to_set = [rating for rating in trakt_ratings if rating['TMDB_ID'] not in [tmdb_rating['TMDB_ID'] for tmdb_rating in tmdb_ratings]]
            trakt_ratings_to_set = [rating for rating in tmdb_ratings if rating['TMDB_ID'] not in [trakt_rating['TMDB_ID'] for trakt_rating in trakt_ratings]]
            tmdb_watchlist_to_set = [item for item in trakt_watchlist if item['TMDB_ID'] not in [tmdb_item['TMDB_ID'] for tmdb_item in tmdb_watchlist]]
            trakt_watchlist_to_set = [item for item in tmdb_watchlist if item['TMDB_ID'] not in [trakt_item['TMDB_ID'] for trakt_item in trakt_watchlist]]
            
            # If remove_watched_from_watchlists_value is true
            if remove_watched_from_watchlists_value:        
                # Get the IDs from watched_content
                watched_content_ids = set(item['TMDB_ID'] for item in watched_content if item['TMDB_ID'])
                        
                # Filter out watched content from trakt_watchlist_to_set
                trakt_watchlist_to_set = [item for item in trakt_watchlist_to_set if item['TMDB_ID'] not in watched_content_ids]
                # Filter out watched content from trakt_watchlist_to_set
                tmdb_watchlist_to_set = [item for item in tmdb_watchlist_to_set if item['TMDB_ID'] not in watched_content_ids]
                
                # Find items to remove from trakt_watchlist
                trakt_watchlist_items_to_remove = [item for item in trakt_watchlist if item['TMDB_ID'] in watched_content_ids]
                # Find items to remove from tmdb_watchlist
                tmdb_watchlist_items_to_remove = [item for item in tmdb_watchlist if item['TMDB_ID'] in watched_content_ids]
            
            # If sync_watchlist_value is true
            if sync_watchlist_value:

                # Set TMDB Watchlist Items
                if tmdb_watchlist_to_set:
                    print('Setting TMDB Watchlist Items')
                    
                    # Fetch Account ID
                    response = EH.make_tmdb_request('https://api.themoviedb.org/3/account')
                    json_data = json.loads(response.text)
                    account_id = json_data['id']
                    
                    # Count the total number of items
                    num_items = len(tmdb_watchlist_to_set)
                    item_count = 0
                    
                    for item in tmdb_watchlist_to_set:
                        item_count += 1
                        print(f" - Adding item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to TMDB Watchlist (TMDB ID: {item['TMDB_ID']})")
                        payload = {}  # Add any additional payload parameters if required
                        if item['Type'] == 'movie':
                            url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
                            payload['media_type'] = "movie"
                            payload['media_id'] = item['TMDB_ID']
                            payload['watchlist'] = True
                            response = EH.make_tmdb_request(url, payload=payload)

                        elif item['Type'] == 'show':
                            url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
                            payload['media_type'] = "tv"
                            payload['media_id'] = item['TMDB_ID']
                            payload['watchlist'] = True
                            response = EH.make_tmdb_request(url, payload=payload)
                        
                        if response is None:
                            error_message = f"Failed to add item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to TMDB Watchlist (TMDB ID: {item['TMDB_ID']})"
                            print(f"   - {error_message}")
                            EL.logger.error(error_message)
                    
                    print('Setting TMDB Watchlist Items Complete')
                else:
                    print('No TMDB Watchlist Items To Set')

                # Set Trakt Watchlist Items
                if trakt_watchlist_to_set:
                    print('Setting Trakt Watchlist Items')

                    # Count the total number of items
                    num_items = len(trakt_watchlist_to_set)
                    item_count = 0

                    for item in trakt_watchlist_to_set:
                        item_count += 1
                        print(f" - Adding item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to Trakt Watchlist (TMDB ID: {item['TMDB_ID']})")
                        tmdb_id = item['TMDB_ID']
                        media_type = item['Type']  # 'movie', 'show', or 'episode'

                        url = f"https://api.trakt.tv/sync/watchlist"

                        data = {
                            "movies": [],
                            "shows": [],
                            "episodes": []
                        }

                        if media_type == 'movie':
                            data['movies'].append({
                                "ids": {
                                    "tmdb": tmdb_id
                                }
                            })
                        elif media_type == 'show':
                            data['shows'].append({
                                "ids": {
                                    "tmdb": tmdb_id
                                }
                            })
                        elif media_type == 'episode':
                            data['episodes'].append({
                                "ids": {
                                    "tmdb": tmdb_id
                                }
                            })

                        response = EH.make_trakt_request(url, payload=data)
                        
                        if response is None:
                            error_message = f"Failed to add item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to Trakt Watchlist (TMDB ID: {item['TMDB_ID']})"
                            print(f"   - {error_message}")
                            EL.logger.error(error_message)

                    print('Setting Trakt Watchlist Items Complete')
                else:
                    print('No Trakt Watchlist Items To Set')

            # If sync_ratings_value is true
            if sync_ratings_value:
                
                # Set TMDB Ratings
                if tmdb_ratings_to_set:
                    print('Setting TMDB Ratings')
                    
                    # Count the total number of items to rate
                    num_items = len(tmdb_ratings_to_set)
                    item_count = 0
                    
                    # Set TMDB Rating
                    for item in tmdb_ratings_to_set:
                        item_count += 1

                        if item['Type'] == 'movie':
                            payload = {
                                'value': item['Rating']
                            }
                            url = f"https://api.themoviedb.org/3/movie/{item['TMDB_ID']}/rating"
                            print(f" - Rating movie ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on TMDB (TMDB ID: {item['TMDB_ID']})")

                        elif item['Type'] == 'show':
                            payload = {
                                'value': item['Rating']
                            }
                            url = f"https://api.themoviedb.org/3/tv/{item['TMDB_ID']}/rating"
                            print(f" - Rating TV show ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on TMDB (TMDB ID: {item['TMDB_ID']})")

                        elif item['Type'] == 'episode':
                            payload = {
                                'value': item['Rating']
                            }
                            url = f"https://api.themoviedb.org/3/tv/{item['TMDB_ShowID']}/season/{item['Season']}/episode/{item['Episode']}/rating"
                            print(f" - Rating episode ({item_count} of {num_items}): {item['Title']} ({item['Year']}) [S{item['Season']:02d}E{item['Episode']:02d}]: {item['Rating']}/10 on TMDB (TMDB ID: {item['TMDB_ID']})")

                        response = EH.make_tmdb_request(url, payload=payload)
                        
                        if response is None:
                            error_message = f"Failed rating item ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on TMDB (TMDB ID: {item['TMDB_ID']})"
                            print(f"   - {error_message}")
                            EL.logger.error(error_message)

                    print('Setting TMDB Ratings Complete')
                else:
                    print('No TMDB Ratings To Set')

                # Set Trakt Ratings
                if trakt_ratings_to_set:
                    print('Setting Trakt Ratings')

                    # Set the API endpoints
                    rate_url = "https://api.trakt.tv/sync/ratings"
                    
                    # Count the total number of items to rate
                    num_items = len(trakt_ratings_to_set)
                    item_count = 0
                            
                    # Loop through your data table and rate each item on Trakt
                    for item in trakt_ratings_to_set:
                        item_count += 1
                        if item["Type"] == "show":
                            # This is a TV show
                            data = {
                                "shows": [{
                                    "ids": {
                                        "tmdb": item["TMDB_ID"]
                                    },
                                    "rating": item["Rating"]
                                }]
                            }
                            print(f" - Rating TV show ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on Trakt (TMDB ID: {item['TMDB_ID']})")
                        elif item["Type"] == "movie":
                            # This is a movie
                            data = {
                                "movies": [{
                                    "ids": {
                                        "tmdb": item["TMDB_ID"]
                                    },
                                    "rating": item["Rating"]
                                }]
                            }
                            print(f" - Rating movie ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on Trakt (TMDB ID: {item['TMDB_ID']})")
                        elif item["Type"] == "episode":
                            # This is an episode
                            data = {
                                "episodes": [{
                                    "ids": {
                                        "tmdb": item["TMDB_ID"]
                                    },
                                    "rating": item["Rating"]
                                }]
                            }
                            print(f" - Rating episode ({item_count} of {num_items}): {item['Title']} ({item['Year']}) [S{item['Season']:02d}E{item['Episode']:02d}]: {item['Rating']}/10 on Trakt (TMDB ID: {item['TMDB_ID']})")

                        # Make the API call to rate the item
                        response = EH.make_trakt_request(rate_url, payload=data)
                        
                        if response is None:
                            error_message = f"Failed rating item ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on Trakt (TMDB ID: {item['TMDB_ID']})"
                            print(f"   - {error_message}")
                            EL.logger.error(error_message)

                    print('Setting Trakt Ratings Complete')
                else:
                    print('No Trakt Ratings To Set')
            
            # If remove_watched_from_watchlists_value is true
            if remove_watched_from_watchlists_value:
            
                # Remove Watched Items Trakt Watchlist
                if trakt_watchlist_items_to_remove:
                    print('Removing Watched Items From Trakt Watchlist')

                    # Set the API endpoint
                    remove_url = "https://api.trakt.tv/sync/watchlist/remove"

                    # Count the total number of items
                    num_items = len(trakt_watchlist_items_to_remove)
                    item_count = 0

                    # Loop through the items to remove from the watchlist
                    for item in trakt_watchlist_items_to_remove:
                        item_count += 1
                        if item["Type"] == "show":
                            # This is a TV show
                            data = {
                                "shows": [{
                                    "ids": {
                                        "trakt": item["TraktID"]
                                    }
                                }]
                            }
                            print(f" - Removing TV show ({item_count} of {num_items}): {item['Title']} ({item['Year']}) from Trakt Watchlist (TMDB ID: {item['TMDB_ID']})")
                        elif item["Type"] == "movie":
                            # This is a movie
                            data = {
                                "movies": [{
                                    "ids": {
                                        "trakt": item["TraktID"]
                                    }
                                }]
                            }
                            print(f" - Removing movie ({item_count} of {num_items}): {item['Title']} ({item['Year']}) from Trakt Watchlist (TMDB ID: {item['TMDB_ID']})")
                        elif item["Type"] == "episode":
                            # This is an episode
                            data = {
                                "episodes": [{
                                    "ids": {
                                        "trakt": item["TraktID"]
                                    }
                                }]
                            }
                            print(f" - Removing episode ({item_count} of {num_items}): {item['Title']} ({item['Year']}) from Trakt Watchlist (TMDB ID: {item['TMDB_ID']})")

                        # Make the API call to remove the item from the watchlist
                        response = EH.make_trakt_request(remove_url, payload=data)

                        if response is None:
                            error_message = f"Failed removing {item['Type']} ({item_count} of {num_items}): {item['Title']} ({item['Year']}) from Trakt Watchlist (TMDB ID: {item['TMDB_ID']})"
                            print(f"   - {error_message}")
                            EL.logger.error(error_message)

                    print('Removing Watched Items From Trakt Watchlist Complete')
                else:
                    print('No Watched Items To Remove From Trakt Watchlist')

                # Remove Watched Items TMDB Watchlist
                if tmdb_watchlist_items_to_remove:
                    print('Removing Watched Items From TMDB Watchlist')
                    
                    # Fetch Account ID
                    response = EH.make_tmdb_request('https://api.themoviedb.org/3/account')
                    json_data = json.loads(response.text)
                    account_id = json_data['id']
                    
                    # Count the total number of items
                    num_items = len(tmdb_watchlist_items_to_remove)
                    item_count = 0
                    
                    for item in tmdb_watchlist_items_to_remove:
                        item_count += 1
                        print(f" - Removing item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) from TMDB Watchlist (TMDB ID: {item['TMDB_ID']})")
                        payload = {}  # Add any additional payload parameters if required
                        if item['Type'] == 'movie':
                            url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
                            payload['media_type'] = "movie"
                            payload['media_id'] = item['TMDB_ID']
                            payload['watchlist'] = False  # Set watchlist to False to remove the item
                            response = EH.make_tmdb_request(url, payload=payload)

                        elif item['Type'] == 'show':
                            url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
                            payload['media_type'] = "tv"
                            payload['media_id'] = item['TMDB_ID']
                            payload['watchlist'] = False  # Set watchlist to False to remove the item
                            response = EH.make_tmdb_request(url, payload=payload)
                        
                        if response is None:
                            error_message = f"Failed to remove item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) from TMDB Watchlist (TMDB ID: {item['TMDB_ID']})"
                            print(f"   - {error_message}")
                            EL.logger.error(error_message)

                    
                    print('Removing Watched Items From TMDB Watchlist Complete')
                else:
                    print('No Watched Items To Remove From TMDB Watchlist')

            print("TMDBTraktSyncer Complete")
            
        except Exception as e:
            error_message = "An error occurred while running the script."
            EH.report_error(error_message)
            EL.logger.error(error_message, exc_info=True)

if __name__ == '__main__':
    main()