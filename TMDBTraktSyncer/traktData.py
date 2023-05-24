import json
import requests
import urllib.parse
try:
    from TMDBTraktSyncer import errorHandling as EH
except ImportError:
    import errorHandling as EH

def getTraktData():
    # Process Trakt Ratings and Comments
    print('Processing Trakt Data')

    response = EH.make_trakt_request('https://api.trakt.tv/users/me')
    json_data = json.loads(response.text)
    username_slug = json_data['ids']['slug']
    encoded_username = urllib.parse.quote(username_slug)
    
    # Get Trakt Watchlist Items
    response = EH.make_trakt_request(f'https://api.trakt.tv/users/{encoded_username}/watchlist?sort=added,asc')
    json_data = json.loads(response.text)

    trakt_watchlist = []

    for item in json_data:
        if item['type'] == 'movie':
            movie = item.get('movie')
            movie_id = movie.get('ids', {}).get('tmdb')
            trakt_watchlist.append({'Title': movie.get('title'), 'Year': movie.get('year'), 'ID': movie_id, 'Type': 'movie'})
        elif item['type'] == 'show':
            show = item.get('show')
            show_id = show.get('ids', {}).get('tmdb')
            trakt_watchlist.append({'Title': show.get('title'), 'Year': show.get('year'), 'ID': show_id, 'Type': 'show'})

    # Get Trakt Ratings
    response = EH.make_trakt_request(f'https://api.trakt.tv/users/{encoded_username}/ratings')
    json_data = json.loads(response.text)

    movie_ratings = []
    show_ratings = []
    episode_ratings = []

    for item in json_data:
        if item['type'] == 'movie':
            movie = item.get('movie')
            movie_id = movie.get('ids', {}).get('tmdb')
            movie_ratings.append({'Title': movie.get('title'), 'Year': movie.get('year'), 'Rating': item.get('rating'), 'ID': movie_id, 'Type': 'movie'})
        elif item['type'] == 'show':
            show = item.get('show')
            show_id = show.get('ids', {}).get('tmdb')
            show_ratings.append({'Title': show.get('title'), 'Year': show.get('year'), 'Rating': item.get('rating'), 'ID': show_id, 'Type': 'show'})
        elif item['type'] == 'episode':
            show = item.get('show')
            show_title = show.get('title')
            show_tmdb_id = show.get('ids', {}).get('tmdb') if show and 'ids' in show else None
            episode = item.get('episode')
            episode_id = episode.get('ids', {}).get('tmdb')
            episode_title = f'{show_title}: {episode.get("title")}'
            episode_ratings.append({
                'Title': episode_title,
                'Year': episode.get('year'),
                'Rating': item.get('rating'),
                'ID': episode_id,
                'Season': episode.get('season'),
                'Episode': episode.get('number'),
                'ShowID': show_tmdb_id,
                'Type': 'episode'
            })

    trakt_ratings = movie_ratings + show_ratings + episode_ratings

    print('Processing Trakt Data')
    
    return trakt_watchlist, trakt_ratings
