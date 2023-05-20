import json
import requests
import urllib.parse
try:
    from TMDBTraktSyncer import errorHandling as EH
except ImportError:
    import errorHandling as EH

def getTraktRatings(trakt_client_id, trakt_access_token):
    # Get Trakt Ratings
    print('Processing Trakt Ratings')

    response = EH.make_trakt_request('https://api.trakt.tv/users/me')
    json_data = json.loads(response.text)
    username_slug = json_data['ids']['slug']
    encoded_username = urllib.parse.quote(username_slug)
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

    print('Processing Trakt Ratings Complete')
    
    return trakt_ratings
