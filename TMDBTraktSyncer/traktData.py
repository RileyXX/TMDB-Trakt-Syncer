import json
import requests
import urllib.parse
import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from TMDBTraktSyncer import errorHandling as EH
from TMDBTraktSyncer import errorLogger as EL

def get_trakt_encoded_username():
    # Process Trakt Ratings and Comments
    response = EH.make_trakt_request('https://api.trakt.tv/users/me')
    json_data = json.loads(response.text)
    username_slug = json_data['ids']['slug']
    encoded_username = urllib.parse.quote(username_slug)
    return encoded_username

def get_trakt_watchlist(encoded_username):  
    # Get Trakt Watchlist Items
    response = EH.make_trakt_request(f'https://api.trakt.tv/users/{encoded_username}/watchlist?sort=added,asc')
    json_data = json.loads(response.text)

    trakt_watchlist = []

    for item in json_data:
        if item['type'] == 'movie':
            movie = item.get('movie')
            tmdb_movie_id = movie.get('ids', {}).get('tmdb')
            trakt_movie_id = movie.get('ids', {}).get('trakt')
            trakt_watchlist.append({'Title': movie.get('title'), 'Year': movie.get('year'), "TMDB_ID": tmdb_movie_id, 'TraktID': trakt_movie_id, 'Type': 'movie'})
        elif item['type'] == 'show':
            show = item.get('show')
            tmdb_show_id = show.get('ids', {}).get('tmdb')
            trakt_show_id = show.get('ids', {}).get('trakt')
            trakt_watchlist.append({'Title': show.get('title'), 'Year': show.get('year'), "TMDB_ID": tmdb_show_id, 'TraktID': trakt_show_id, 'Type': 'show'})
    
    return trakt_watchlist

def get_trakt_ratings(encoded_username):
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
            movie_ratings.append({'Title': movie.get('title'), 'Year': movie.get('year'), 'Rating': item.get('rating'), "TMDB_ID": movie_id, 'Type': 'movie'})
        elif item['type'] == 'show':
            show = item.get('show')
            show_id = show.get('ids', {}).get('tmdb')
            show_ratings.append({'Title': show.get('title'), 'Year': show.get('year'), 'Rating': item.get('rating'), "TMDB_ID": show_id, 'Type': 'show'})
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
                "TMDB_ID": episode_id,
                'Season': episode.get('season'),
                'Episode': episode.get('number'),
                'TMDB_ShowID': show_tmdb_id,
                'Type': 'episode'
            })

    trakt_ratings = movie_ratings + show_ratings + episode_ratings
    
    return trakt_ratings
    
def get_trakt_watch_history(encoded_username):
    # Get Trakt Watch History
    response = EH.make_trakt_request(f'https://api.trakt.tv/users/{encoded_username}/history?limit=100')
    json_data = json.loads(response.text)
    total_pages = response.headers.get('X-Pagination-Page-Count')

    watched_movies = []
    watched_shows = []
    watched_episodes = []
    seen_ids = set()

    for page in range(1, int(total_pages) + 1):
        response = EH.make_trakt_request(f'https://api.trakt.tv/users/{encoded_username}/history?extended=full', params={'page': page, 'limit': 100})
        json_data = json.loads(response.text)

        for item in json_data:
            if item['type'] == 'movie':
                movie = item.get('movie')
                tmdb_movie_id = movie.get('ids', {}).get('tmdb')
                trakt_movie_id = movie.get('ids', {}).get('trakt')
                if trakt_movie_id and trakt_movie_id not in seen_ids:
                    watched_movies.append({'Title': movie.get('title'), 'Year': movie.get('year'), 'TMDB_ID': tmdb_movie_id, 'TraktID': trakt_movie_id, 'WatchedAt': item.get('watched_at'), 'Type': 'movie'})
                    seen_ids.add(trakt_movie_id)
            elif item['type'] == 'episode':
                show = item.get('show')
                tmdb_show_id = show.get('ids', {}).get('tmdb')
                trakt_show_id = show.get('ids', {}).get('trakt')
                show_status = show.get('status')
                aired_episodes = show.get('aired_episodes')
                
                if trakt_show_id and trakt_show_id not in seen_ids:
                    watched_shows.append({'Title': show.get('title'), 'Year': show.get('year'), 'TMDB_ID': tmdb_show_id, 'TraktID': trakt_show_id, 'ShowStatus': show_status, 'AiredEpisodes': aired_episodes, 'WatchedAt': item.get('watched_at'), 'Type': 'show'})
                    seen_ids.add(trakt_show_id)

                show_title = show.get('title')
                episode = item.get('episode')
                season_number = episode.get('season')
                episode_number = episode.get('number')
                tmdb_episode_id = episode.get('ids', {}).get('tmdb')
                trakt_episode_id = episode.get('ids', {}).get('trakt')
                episode_title = f'{show_title}: {episode.get("title")}'
                episode_year = datetime.datetime.strptime(episode.get('first_aired'), "%Y-%m-%dT%H:%M:%S.%fZ").year if episode.get('first_aired') else None
                watched_at = item.get('watched_at')
                if trakt_episode_id and trakt_episode_id not in seen_ids:
                    watched_episodes.append({'Title': episode_title, 'Year': episode_year, 'TMDB_ID': tmdb_episode_id, 'TraktID': trakt_episode_id, 'TraktShowID': trakt_show_id, 'SeasonNumber': season_number, 'EpisodeNumber': episode_number, 'WatchedAt': watched_at, 'Type': 'episode'})
                    seen_ids.add(trakt_episode_id)

    # Filter watched_shows for completed shows where 80% or more of the show has been watched AND where the show's status is "ended" or "cancelled"
    filtered_watched_shows = []
    for show in watched_shows:
        trakt_show_id = show['TraktID']
        show_status = show['ShowStatus']
        aired_episodes = show['AiredEpisodes']
        episode_numbers = [episode['EpisodeNumber'] for episode in watched_episodes if episode['Type'] == 'episode' and episode['TraktShowID'] == trakt_show_id]
        unique_watched_episode_count = len(episode_numbers)
        
        if (show_status.lower() in ['ended', 'cancelled', 'canceled']) and (unique_watched_episode_count >= 0.8 * int(aired_episodes)):
            filtered_watched_shows.append(show)

    # Update watched_shows with the filtered results
    watched_shows = filtered_watched_shows

    trakt_watch_history = watched_movies + watched_shows + watched_episodes
    
    return trakt_watch_history