import ast
import math
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# dictionary of genres and their subgenres
genre_dict = {
    "techno": ["techhouse", "edm", "house", "rave", "dubstep", "melodictechno", "techno", "dance", "electronic", "ghettotech"],
    "rave": ["edm", "rave", "techno", "dance", "electronic"],
    "house": ["techhouse", "edm", "house", "rave", "dance", "electronic", "deephouse"],
    "trance": ["edm", "trance", "rave", "psytrance", "dance", "electronic"],
    "dubstep": ["edm", "dubstep", "dance", "electronic", "bass"],
    "drum and bass": ["edm", "rave", "drum and bass", "dance", "electronic"],
    "gabber": ["edm", "dance", "gabber", "electronic"],
    "hardgroove": ["rave", "hardgroove", "techno", "dance", "electronic"],
    "hardstyle": ["edm", "rave", "hardstyle", "dance", "electronic", "techno"],
    "psytrance": ["edm", "trance", "psytrance", "dance", "electronic"],
    "synthpop": ["indie", "synthpop", "grunge", "alternative"],
    "trap": ["hip hop", "trap", "street", "rap"],
    "hip hop": ["hip hop", "street", "rap"],
    "hiphop": ["hip hop", "street", "rap"],
    "rap": ["hip hop", "street", "rap"],
    "pop": ["electropop", "synthpop", "pop", "indiepop", "dance"],
    "dance": ["pop", "dance"],
    "rock": ["classic rock", "alternative", "hard rock", "metal", "rock", "psychedelic", "punk", "grunge", "indie"],
    "metal": ["death metal", "hard rock", "metal", "rock", "heavy metal", "black metal"],
    "hard rock": ["rock", "hard rock", "metal"],
    "country": ["americana", "folk", "bluegrass", "country"],
    "bluegrass": ["bluegrass", "country"],
    "jazz": ["smooth jazz", "swing", "blues", "jazz fusion", "jazz"],
    "blues": ["rhythm and blues", "jazz", "soul", "blues"],
    "classical": ["orchestral", "baroque", "classical", "opera", "symphony"],
    "orchestral": ["orchestral", "classical"],
    "electronic": ["downtempo", "edm", "house", "ambient", "techno", "dance", "electronic"],
    "edm": ["edm", "dance", "electronic"],
    "indie": ["indie", "lo-fi", "indie rock", "alternative"],
    "alternative": ["alternative", "indie"],
    "folk": ["folk rock", "acoustic", "singer-songwriter", "folk"],
    "acoustic": ["acoustic", "folk"],
    "r&b": ["r&b", "soul"],
    "soul": ["r&b", "soul"],
    "reggae": ["ska", "dub", "reggae"],
    "ska": ["ska", "reggae", "rocksteady"],
    "punk": ["punk", "emo"],
    "emo": ["punk", "emo"],
    "latin": ["salsa", "reggaeton", "samba", "latin", "tango", "brazilian"],
    "salsa": ["salsa", "latin"],
    "gospel": ["spiritual", "gospel"],
    "spiritual": ["spiritual", "gospel"],
    "funk": ["funk", "disco"],
    "disco": ["funk", "disco"],
    "world": ["international", "ethnic", "global", "world"],
    "international": ["international", "world"],
    "new age": ["ambient", "new age"],
    "ambient": ["ambient", "new age"],
    "soundtrack": ["score", "soundtrack"],
    "score": ["score", "soundtrack"],
    "parody": ["parody", "comedy"],
    "mood": ["easy listening", "mood"],
    "brazilian": ["brazilian", "samba"],
    "samba": ["brazilian", "samba"],
    "fado": ["portuguese", "fado"],
    "portuguese": ["portuguese", "fado"],
    "tango": ["argentinian", "tango"],
    "hip hop / rap": ["hip hop", "trap", "street", "rap", "hiphop"],
    "soul / r&b": ["r&b", "motown", "funk", "soul"],
    "ambient / new age": ["chillout", "ambient", "downtempo", "new age"],
    "gospel / spiritual": ["spiritual", "christian", "worship", "gospel"],
    "funk / disco": ["groove", "funk", "dance", "disco"],
    "punk / emo": ["hardcore", "punk", "skate punk", "emo"],
    "electronic dance": ["edm", "house", "techno", "dance", "electronic"],
}

def setup_db_conn():
    # create a connection to the PostgreSQL database
    engine = create_engine('postgresql://postgres:system@localhost:5432/spotevent')
    return engine


def import_prep_data(username, engine):
    # select all songs matching user and filter for ones with a popularity over 45 and genre
    song_data = pd.read_sql("""
        SELECT * FROM backend_track
        WHERE popularity > 35
        AND users LIKE %s
        AND genres IS NOT NULL AND genres != '[]'
    """, engine, params=('%' + username + '%',))

    # select all artists matching user and filter for ones with a genre
    artist_data = pd.read_sql("""
        SELECT * FROM backend_artist
        WHERE users LIKE %s
        AND genres IS NOT NULL AND genres != ''
    """, engine, params=('%' + username + '%',))

    # get the user's data
    user_data = pd.read_sql("""
        SELECT * FROM backend_user
        WHERE username = %s
    """, engine, params=(username,))

    # get all events
    event_data = pd.read_sql('SELECT * FROM backend_event', engine)

    # get all venues
    venue_data = pd.read_sql('SELECT * FROM backend_venue', engine)
    
    # convert the string representations of lists into actual lists
    song_data['genres'] = song_data['genres'].apply(ast.literal_eval)
    artist_data['genres'] = artist_data['genres'].apply(ast.literal_eval)
    # event_data['tags'] is already a list, so no need to convert it

    # join the elements of each list into a single string
    song_data['genres'] = song_data['genres'].apply(','.join)
    artist_data['genres'] = artist_data['genres'].apply(','.join)

    # get the user's genres from the SPOTIFY song and artist data
    user_song_genres = song_data['genres']
    user_artist_genres = artist_data['genres']

    # concat genres from both song and artist data
    combined_genres_series = pd.concat([user_song_genres, user_artist_genres])

    # convert the series to a comma seperated list
    combined_genres_list = ','.join(combined_genres_series.tolist()).split(',')

    # remove duplicates
    unique_combined_genres = list(set(combined_genres_list))

    # now split user data into quiz preferences
    user_quiz_venues = user_data['venue_preferences']
    user_quiz_genres = user_data['genre_preferences']
    user_quiz_pricerange = user_data['price_range']
    user_saved_recommendations = user_data['recommended_events']

    # combine user's combined song/artist genres with their quiz genres
    all_user_genres = list(set(unique_combined_genres + user_quiz_genres.tolist()))

    # convert pricerange from Series to list
    user_quiz_pricerange_list = user_quiz_pricerange.tolist()
    # convert list of strings to list of integers
    price_range = ast.literal_eval(user_quiz_pricerange_list[0])
    min_price, max_price = price_range

    # convert event_data and venue_data Dataframe to list of dictionaries
    events = event_data.to_dict('records')
    venues = venue_data.to_dict('records')

    # attach venue names to events
    for event in events:
        for venue in venues:
            if event['venue_id'] == venue['id']:
                event['venue_name'] = venue['name']
                break

    # return song_data, artist_data, event_data, user_quiz_venues, user_quiz_genres, events, min_price, max_price, user_saved_recommendations, unique_combined_genres
    return all_user_genres, user_quiz_venues, events, min_price, max_price

def map_user_genres(user_genres, genre_dict):
    """
    Map user's Spotify genres to event genres using genre_dict.
    
    Parameters:
    - user_genres: List of genres from Spotify.
    - genre_dict: Dictionary mapping Spotify genres to event genres.
    
    Returns:
    - List of mapped genres.
    """
    mapped_genres = [genre_dict.get(genre, genre) for genre in user_genres]
    return list(set(tuple(i) for i in mapped_genres))  # remove duplicates to get unique mapped genres.

def calculate_genre_similarity(user_genres, event_genres):
    """
    Calculate a genre similarity score for an event based on user's mapped genres.
    
    Parameters:
    - user_mapped_genres: List of user's preferred genres, mapped to broader categories.
    - event_genres: List of event's genres.
    
    Returns:
    - A similarity score (int).
    """
    # Count how many of the event's genres are in the user's preferred genres
    match_count = sum(genre in user_genres for genre in event_genres)
    # Simple score: number of matches. Could be refined with more complex logic.
    return match_count

def score_event(event, user_preferences):
    """
    Score an event based on user preferences, including genre similarity, venue preference, and price sensitivity.
    
    Parameters:
    - event: A dictionary representing an event, including 'genres', 'venue_name', and 'price'.
    - user_preferences: A dictionary of user preferences, including 'mapped_genres', 'preferred_venues', 'min_price', and 'max_price'.
    
    Returns:
    - An overall score for the event (int).
    """
    genre_weight = 0.5
    venue_weight = 0.3
    price_weight = 0.2

    genre_score = calculate_genre_similarity(user_preferences['mapped_genres'], event['tags'])
    venue_score = 1 if event['venue_name'] in user_preferences['preferred_venues'] else 0
    price_score = 1 if user_preferences['min_price'] <= event['price'] <= user_preferences['max_price'] else 0
    
    # Example scoring logic: sum of scores. Adjust weighting as needed.
    # return genre_score + venue_score + price_score
    # Non-linear scoring
    return math.log(genre_score*genre_weight + 1) + venue_score*venue_weight + price_score*price_weight

def recommend_events(events, user_preferences):
    """
    Recommend events based on scores calculated from user preferences.
    
    Parameters:
    - events: List of dictionaries, each representing an event.
    - user_preferences: A dictionary of user preferences.
    
    Returns:
    - List of recommended events, sorted by their score.
    """
    for event in events:
        event['score'] = score_event(event, user_preferences)
    
    # Sort events by score in descending order
    recommended_events = sorted(events, key=lambda x: x['score'], reverse=True)
    
    return recommended_events

def recommend_top_20_events(recommended_events):
    """
    Recommend top 20 events from the list of recommended events.
    
    Parameters:
    - recommended_events: List of recommended events, sorted by score.
    
    Returns:
    - List of top 20 event IDs.
    """
    top_20_events = recommended_events[:20]
    top_20_events_ids = [event['event_id'] for event in top_20_events]
    
    return top_20_events_ids, top_20_events


def main(username):
    # Setup database connection
    engine = setup_db_conn()

    # song_data, artist_data, event_data, user_quiz_venues, user_quiz_genres, events, min_price, max_price, user_saved_recommendations, unique_combined_genres = import_prep_data(username, engine)

    # Import and prepare data
    all_user_genres, user_quiz_venues, events, min_price, max_price = import_prep_data(username, engine)

    # Map user's Spotify genres to event genres
    # user_spotify_mapped_genres = map_user_genres(unique_combined_genres, genre_dict)

    # Map user's Spotify genres to event genres
    # user_preference_mapped_genres = map_user_genres(user_quiz_genres, genre_dict)

    mapped_genres = map_user_genres(all_user_genres, genre_dict)

    # User preferences
    user_preferences = {
        'mapped_genres': mapped_genres,
        'preferred_venues': user_quiz_venues,
        'min_price': min_price,
        'max_price': max_price
    }

    # Recommend events
    recommended_events = recommend_events(events, user_preferences)

    # Print recommended events
    for event in recommended_events:
        print(f"Event: {event['name']} (Score: {event['score']})")

    top_20_events_ids, top_20_events = recommend_top_20_events(recommended_events)
    
    # print top 20 event IDs from event list
    print("Top 20 Event IDs: ", top_20_events_ids)
    print("Top 20 Events: ", pd.DataFrame(top_20_events))


    return top_20_events_ids

if __name__ == "__main__":
    main('m.tweedy')
    print("Recommendations generated successfully.")