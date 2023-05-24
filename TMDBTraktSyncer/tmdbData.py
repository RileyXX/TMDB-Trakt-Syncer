import requests
import json
import time
try:
    from TMDBTraktSyncer import errorHandling as EH
except ImportError:
    import errorHandling as EH

def fetch_data(url):
    response = EH.make_tmdb_request(url)
    json_data = json.loads(response.text)
    results = json_data['results']
    total_pages = json_data['total_pages']
    current_page = json_data['page']
    return results, total_pages, current_page

def getTMDBRatings():
    print('Processing TMDB Data')

    # Fetch Account ID
    response = EH.make_tmdb_request('https://api.themoviedb.org/3/account')
    json_data = json.loads(response.text)
    account_id = json_data['id']
    
    # Fetch Movies Watchlist
    movie_watchlist = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/watchlist/movies?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for movie in results:
            movie_watchlist.append({'Title': movie['title'], 'Year': movie['release_date'][:4], 'ID': movie['id'], 'Type': 'movie'})
        
        page += 1

    # Fetch TV Show Watchlist
    show_watchlist = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/watchlist/tv?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for show in results:
            show_watchlist.append({'Title': show['name'], 'Year': show['first_air_date'][:4], 'ID': show['id'], 'Type': 'show'})
        
        page += 1

    tmdb_watchlist = movie_watchlist + show_watchlist

    # Fetch Movie Ratings
    movie_ratings = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/movies?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for movie in results:
            movie_ratings.append({'Title': movie['title'], 'Year': movie['release_date'][:4], 'Rating': movie['rating'], 'ID': movie['id'], 'Type': 'movie'})
        
        page += 1

    # Fetch TV Show Ratings
    show_ratings = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/tv?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for show in results:
            show_ratings.append({'Title': show['name'], 'Year': show['first_air_date'][:4], 'Rating': show['rating'], 'ID': show['id'], 'Type': 'show'})
        
        page += 1

    # Fetch Episode Ratings
    episode_ratings = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        url = f'https://api.themoviedb.org/3/account/{account_id}/rated/tv/episodes?page={page}'
        results, total_pages, _ = fetch_data(url)
        
        for episode in results:
            show_id = episode['show_id']
            response = EH.make_tmdb_request(f'https://api.themoviedb.org/3/tv/{show_id}')
            show_info = json.loads(response.text)
            show_name = show_info.get('name', 'Show Name Not Found')
            episode_title = f"{show_name}: {episode.get('name', 'Episode Name Not Found')}"
            episode_ratings.append({
                'Title': episode_title,
                'Year': episode.get('air_date', '')[:4],
                'Rating': episode.get('rating'),
                'ID': episode.get('id'),
                'Season': episode.get('season_number'),
                'Episode': episode.get('episode_number'),
                'ShowID': show_id,
                'Type': 'episode'
            })
            
            page += 1

    tmdb_ratings = movie_ratings + show_ratings + episode_ratings

    print('Processing TMDB Data Complete')

    return tmdb_watchlist, tmdb_ratings
