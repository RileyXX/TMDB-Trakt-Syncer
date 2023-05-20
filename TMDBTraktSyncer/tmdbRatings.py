import requests
import json
import time
try:
    from TMDBTraktSyncer import errorHandling
except:
    import errorHandling

def fetch_data(url):
    response = errorHandling.make_tmdb_request(url)
    json_data = json.loads(response.text)
    results = json_data['results']
    total_pages = json_data['total_pages']
    current_page = json_data['page']
    return results, total_pages, current_page

def getTMDBRatings(tmdb_v4_token):
    # Get TMDB Ratings
    print('Processing TMDB Ratings')

    response = errorHandling.make_tmdb_request('https://api.themoviedb.org/3/account')
    json_data = json.loads(response.text)
    account_id = json_data['id']

    movie_ratings = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/movies?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for movie in results:
            movie_ratings.append({'Title': movie['title'], 'Year': movie['release_date'][:4], 'Rating': movie['rating'], 'ID': movie['id'], 'Type': 'movie'})
        
        page += 1
        time.sleep(1)

    # Fetch TV show ratings
    show_ratings = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/tv?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for show in results:
            show_ratings.append({'Title': show['name'], 'Year': show['first_air_date'][:4], 'Rating': show['rating'], 'ID': show['id'], 'Type': 'show'})
        
        page += 1
        time.sleep(1)

    # Fetch episode ratings
    episode_ratings = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/tv/episodes?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for episode in results:
            show_id = episode['show_id']
            response = errorHandling.make_tmdb_request(f'https://api.themoviedb.org/3/tv/{show_id}')
            show_info = json.loads(response.text)
            show_name = show_info['name'] if 'name' in show_info else ''
            episode_title = f"{show_name}: {episode['name']}"
            episode_ratings.append({
                'Title': episode_title,
                'Year': episode['air_date'][:4],
                'Rating': episode['rating'],
                'ID': episode['id'],
                'Season': episode['season_number'],
                'Episode': episode['episode_number'],
                'ShowID': show_id,
                'Type': 'episode'
            })
        
        page += 1
        time.sleep(1)

    tmdb_ratings = movie_ratings + show_ratings + episode_ratings

    print('Processing TMDB Ratings Complete')

    return tmdb_ratings
