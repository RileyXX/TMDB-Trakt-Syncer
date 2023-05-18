import json
import requests
import time
try:
    from TMDBTraktSyncer import verifyCredentials
    from TMDBTraktSyncer import traktRatings
    from TMDBTraktSyncer import tmdbRatings
    from TMDBTraktSyncer import errorHandling
except:
    import verifyCredentials
    import traktRatings
    import tmdbRatings
    import errorHandling


def main():
    try:

        #Get credentials
        trakt_client_id = verifyCredentials.trakt_client_id
        trakt_client_secret = verifyCredentials.trakt_client_secret
        trakt_access_token = verifyCredentials.trakt_access_token
        tmdb_v4_token = verifyCredentials.tmdb_v4_token
            
        trakt_ratings = traktRatings.getTraktRatings(trakt_client_id, trakt_access_token)
        tmdb_ratings = tmdbRatings.getTMDBRatings(tmdb_v4_token)

        #Get trakt and tmdb ratings and filter out trakt ratings with missing tmdb id
        trakt_ratings = [rating for rating in trak_tratings if rating['ID'] is not None]
        tmdb_ratings = [rating for rating in tmdb_ratings if rating['ID'] is not None]
        #Filter out ratings already set
        tmdb_ratings_to_set = [rating for rating in trakt_ratings if rating['ID'] not in [tmdb_rating['ID'] for tmdb_rating in tmdb_ratings]]
        trakt_ratings_to_set = [rating for rating in tmdb_ratings if rating['ID'] not in [trakt_rating['ID'] for trakt_rating in trakt_ratings]]

        if tmdb_ratings_to_set:
            print('Setting TMDB Ratings')
            
            # Count the total number of items to rate
            num_items = len(tmdb_ratings_to_set)
            item_count = 0
            
            # Set TMDB Rating
            for item in tmdb_ratings_to_set:
                item_count += 1

                headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json;charset=utf-8',
                    'Authorization': f'Bearer {tmdb_v4_token}'
                }
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

                response = requests.post(url, headers=headers, json=payload)

                while response.status_code == 429:
                    print("Rate limit exceeded. Waiting for 1 second...")
                    time.sleep(1)
                    response = requests.post(url, headers=headers, json=payload)
                if response.status_code != 201:
                    print(f"Error rating {item}: {response.content}")

            print('Setting TMDB Ratings Complete')
        else:
            print('No TMDB Ratings To Set')

        if trakt_ratings_to_set:
            print('Setting Trakt Ratings')

            # Set the API endpoints
            oauth_url = "https://api.trakt.tv/oauth/token"
            rate_url = "https://api.trakt.tv/sync/ratings"

            # Set the headers
            headers = {
                "Content-Type": "application/json",
                "trakt-api-version": "2",
                "trakt-api-key": trakt_client_id,
                "Authorization": f"Bearer {trakt_access_token}"
            }
            
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
                response = requests.post(rate_url, headers=headers, json=data)
                time.sleep(1)
                while response.status_code == 429:
                    print("Rate limit exceeded. Waiting for 1 second...")
                    time.sleep(1)
                    response = requests.post(rate_url, headers=headers, json=data)
                if response.status_code != 201:
                    print(f"Error rating {item}: {response.content}")

            print('Setting Trakt Ratings Complete')
        else:
            print('No Trakt Ratings To Set')

    except Exception as e:
        error_message = "An error occurred while running the script."
        errorHandling.report_error(error_message)

if __name__ == '__main__':
    main()