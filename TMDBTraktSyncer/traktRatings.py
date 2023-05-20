import json
import requests
try:
    from TMDBTraktSyncer import errorHandling
except:
    import errorHandling

def getTraktRatings(trakt_client_id, trakt_access_token):
    # Get Trakt Ratings
    print('Getting Trakt Ratings')

    response = errorHandling.make_trakt_request('https://api.trakt.tv/users/me')
    json_data = json.loads(response.text)
    username = json_data['username']
    response = errorHandling.make_trakt_request(f'https://api.trakt.tv/users/{username}/ratings')
    json_data = json.loads(response.text)

    movie_ratings = []
    show_ratings = []
    episode_ratings = []

    for item in json_data:
        if item['type'] == 'movie':
            movie = item['movie']
            movie_id = movie['ids']['tmdb']
            movie_ratings.append({'Title': movie['title'], 'Year': movie['year'], 'Rating': item['rating'], 'ID': movie_id, 'Type': 'movie'})
        elif item['type'] == 'show':
            show = item['show']
            show_id = show['ids']['tmdb']
            show_ratings.append({'Title': show['title'], 'Year': show['year'], 'Rating': item['rating'], 'ID': show_id, 'Type': 'show'})
        elif item['type'] == 'episode':
            show = item['show']
            show_title = show['title']
            show_tmdb_id = show['ids']['tmdb'] if 'ids' in show and 'tmdb' in show['ids'] else None
            episode = item['episode']
            episode_id = episode['ids']['tmdb']
            episode_title = f'{show_title}: {episode["title"]}'
            episode_ratings.append({
                'Title': episode_title,
                'Year': episode.get('year'),
                'Rating': item['rating'],
                'ID': episode_id,
                'Season': episode['season'],
                'Episode': episode['number'],
                'ShowID': show_tmdb_id,
                'Type': 'episode'
            })

    trakt_ratings = movie_ratings + show_ratings + episode_ratings

    print('Getting Trakt Ratings Complete')
    
    return trakt_ratings
