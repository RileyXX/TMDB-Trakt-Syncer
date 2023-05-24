import json
import requests
import time
try:
    from TMDBTraktSyncer import verifyCredentials as VC
    from TMDBTraktSyncer import traktData
    from TMDBTraktSyncer import tmdbData
    from TMDBTraktSyncer import errorHandling as EH
except ImportError:
    import verifyCredentials as VC
    import traktData
    import tmdbData
    import errorHandling as EH


def main():
    try:
            
        trakt_watchlist, trakt_ratings = traktData.getTraktData()
        tmdb_watchlist, tmdb_ratings = tmdbData.getTMDBRatings()

        #Get trakt and tmdb ratings and filter out trakt ratings with missing tmdb id
        trakt_ratings = [rating for rating in trakt_ratings if rating['ID'] is not None]
        tmdb_ratings = [rating for rating in tmdb_ratings if rating['ID'] is not None]
        trakt_watchlist = [item for item in trakt_watchlist if item['ID'] is not None]
        tmdb_watchlist = [item for item in tmdb_watchlist if item['ID'] is not None]
        #Filter out ratings already set
        tmdb_ratings_to_set = [rating for rating in trakt_ratings if rating['ID'] not in [tmdb_rating['ID'] for tmdb_rating in tmdb_ratings]]
        trakt_ratings_to_set = [rating for rating in tmdb_ratings if rating['ID'] not in [trakt_rating['ID'] for trakt_rating in trakt_ratings]]
        tmdb_watchlist_to_set = [item for item in trakt_watchlist if item['ID'] not in [tmdb_item['ID'] for tmdb_item in tmdb_watchlist]]
        trakt_watchlist_to_set = [item for item in tmdb_watchlist if item['ID'] not in [trakt_item['ID'] for trakt_item in trakt_watchlist]]
        
        # If sync_watchlist_value is true
        if VC.sync_watchlist_value:

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
                    payload = {}  # Add any additional payload parameters if required
                    if item['Type'] == 'movie':
                        url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
                        payload['media_type'] = "movie"
                        payload['media_id'] = item['ID']
                        payload['watchlist'] = True
                        response = EH.make_tmdb_request(url, payload=payload)

                    elif item['Type'] == 'show':
                        url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
                        payload['media_type'] = "tv"
                        payload['media_id'] = item['ID']
                        payload['watchlist'] = True
                        response = EH.make_tmdb_request(url, payload=payload)
                    if response:
                        print(f"Adding item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to TMDB Watchlist")
                    else:
                        print(f"Failed to add item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to TMDB Watchlist (TMDB ID: {item['ID']})")
                
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
                    tmdb_id = item['ID']
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
                    if response:
                        print(f"Adding item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to Trakt Watchlist")
                    else:
                        print(f"Failed to add item ({item_count} of {num_items}): {item['Title']} ({item['Year']}) to Trakt Watchlist (TMDB ID: {item['ID']})")
                        print("Error Response:", response.content, response.status_code)

                print('Trakt Watchlist Items Set Successfully')
            else:
                print('No Trakt Watchlist Items To Set')

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
                    url = f"https://api.themoviedb.org/3/movie/{item['ID']}/rating"
                    print(f"Rating movie ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on TMDB")

                elif item['Type'] == 'show':
                    payload = {
                        'value': item['Rating']
                    }
                    url = f"https://api.themoviedb.org/3/tv/{item['ID']}/rating"
                    print(f"Rating TV show ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on TMDB")

                elif item['Type'] == 'episode':
                    payload = {
                        'value': item['Rating']
                    }
                    url = f"https://api.themoviedb.org/3/tv/{item['ShowID']}/season/{item['Season']}/episode/{item['Episode']}/rating"
                    print(f"Rating episode ({item_count} of {num_items}): {item['Title']} ({item['Year']}) [S{item['Season']:02d}E{item['Episode']:02d}]: {item['Rating']}/10 on TMDB")

                response = EH.make_tmdb_request(url, payload=payload)

            print('Setting TMDB Ratings Complete')
        else:
            print('No TMDB Ratings To Set')

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
                                "tmdb": item["ID"]
                            },
                            "rating": item["Rating"]
                        }]
                    }
                    print(f"Rating TV show ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on Trakt")
                elif item["Type"] == "movie":
                    # This is a movie
                    data = {
                        "movies": [{
                            "ids": {
                                "tmdb": item["ID"]
                            },
                            "rating": item["Rating"]
                        }]
                    }
                    print(f"Rating movie ({item_count} of {num_items}): {item['Title']} ({item['Year']}): {item['Rating']}/10 on Trakt")
                elif item["Type"] == "episode":
                    # This is an episode
                    data = {
                        "episodes": [{
                            "ids": {
                                "tmdb": item["ID"]
                            },
                            "rating": item["Rating"]
                        }]
                    }
                    print(f"Rating episode ({item_count} of {num_items}): {item['Title']} ({item['Year']}) [S{item['Season']:02d}E{item['Episode']:02d}]: {item['Rating']}/10 on Trakt")

                # Make the API call to rate the item
                response = EH.make_trakt_request(rate_url, payload=data)

            print('Setting Trakt Ratings Complete')
        else:
            print('No Trakt Ratings To Set')

    except Exception as e:
        error_message = "An error occurred while running the script."
        EH.report_error(error_message)

if __name__ == '__main__':
    main()