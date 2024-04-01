import ast
import math
import pandas as pd
from sqlalchemy import create_engine

# TODO : have check for if user has no preferences

# TODO : cosine similarity
# TODO : TF-IDF
# TODO : K-means clustering


def clean_and_standardize(data):
    """
    Clean and standardize data by stripping whitespace and converting to lowercase.
    """
    # if data is a string, strip whitespace and convert to lowercase
    if isinstance(data, str):
        return data.strip().lower()
    # else if data is a list, strip whitespace and convert each element to lowercase
    elif isinstance(data, list):
        cleaned_data = [element.strip().lower() for element in data if isinstance(element, str)]
        return cleaned_data
    return data


def deserialize_and_clean(data_str):
    """
    Deserialize and clean a string representation of a list of data elements.
    """
    try:
        # convert string representation of list to actual list
        data_list = ast.literal_eval(data_str)
        # clean and standardize the list elements
        if isinstance(data_list, list):
            return clean_and_standardize(data_list)
    except ValueError:
        print("Error deserializing or cleaning data:", data_str)
    return []


def map_user_genres(user_genres, genre_dict):
    """
    Map user genres to broader categories using a genre dictionary mapping.
    """
    mapped_genres = []
    for genre in user_genres:
        if genre in genre_dict:
            mapped_genres.extend(genre_dict[genre])
    return list(set(mapped_genres))


def import_prep_data(username, engine):
    """
    Import user data from database and prepare it for recommendation processing.
    """
    song_data_query = """
        SELECT * FROM backend_track
        WHERE popularity > 35
        AND users LIKE %s
        AND genres IS NOT NULL AND genres != '[]'
    """
    song_data = pd.read_sql(song_data_query, engine, params=('%' + username + '%',))
    user_song_genres = song_data['genres'].apply(lambda x: deserialize_and_clean(x)).sum()

    # select all artists matching user and filter for ones with a genre
    artist_data = """
        SELECT * FROM backend_artist
        WHERE users LIKE %s
        AND genres IS NOT NULL AND genres != ''
    """
    artist_data = pd.read_sql(artist_data, engine, params=('%' + username + '%',))
    user_artist_genres = artist_data['genres'].apply(lambda x: deserialize_and_clean(x)).sum()

    user_data_query = f"SELECT * FROM backend_user WHERE username = '{username}'"
    user_data = pd.read_sql(user_data_query, engine)

    events_query = "SELECT * FROM backend_event"
    events = pd.read_sql(events_query, engine).to_dict('records')

    venues_query = "SELECT * FROM backend_venue"
    venues = pd.read_sql(venues_query, engine).to_dict('records')

    # if user data exists, prepare it for recommendation processing
    if not user_data.empty:
        user_row = user_data.iloc[0]
        user_quiz_venues = deserialize_and_clean(user_row['venue_preferences'])
        user_quiz_genres = deserialize_and_clean(user_row['genre_preferences'])
        print("user_quiz_genres: ", user_quiz_genres)
        print("user_quiz_venues: ", user_quiz_venues)
        print("price_range: ", user_row['price_range'])
        min_price, max_price = ast.literal_eval(user_row['price_range'])
        
        # map user genres to broader categories
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
        
        combined_genres = user_song_genres + user_artist_genres + user_quiz_genres
        user_mapped_genres = map_user_genres(combined_genres, genre_dict)
        # user_mapped_genres = map_user_genres(user_quiz_genres, genre_dict)

        # process event tags
        for event in events:
            event['tags'] = clean_and_standardize(event['tags'].split(','))

        # attach venue names to events
        for event in events:
            for venue in venues:
                if event['venue_id'] == venue['id']:
                    event['venue_name'] = venue['name']
                    break

        return {
            'user_quiz_venues': user_quiz_venues,
            'user_mapped_genres': user_mapped_genres,
            'min_price': min_price,
            'max_price': max_price,
            'events': events
        }
    else:
        return None


def calculate_genre_similarity(user_genres, event_genres):
    """
    Calculate a normalized genre similarity score for an event based on user's mapped genres.

    """
    # ensure user_genres is a list
    if isinstance(user_genres, str):
        user_genres = [user_genres]  # convert to list if it's a string
    
    # ensure event_genres is a list
    if isinstance(event_genres, str):
        event_genres = [event_genres]  # convert to list if it's a string

    if not user_genres or not event_genres:
        return 0  # avoid division by zero if either list is empty

    # count how many of event's genres are in user's preferred genres
    match_count = sum(genre in user_genres for genre in event_genres)
    
    # normalize the score by the total number of unique genres considered
    total_genres = len(set(user_genres + event_genres))
    
    # normalize score to be a fraction between 0 and 1
    similarity_score = match_count / total_genres if total_genres else 0
    
    return similarity_score


def score_event(event, user_data):
    """
    Score an event based on user preferences, including genre similarity, venue preference, and price sensitivity.
    """
    genre_weight = 0.6
    price_weight = 0.3 # Adjusted to ensure weights sum to 1
    venue_weight = 0.1

    genre_score = calculate_genre_similarity(user_data['user_mapped_genres'], event['tags'])
    venue_score = 1 if event['venue_name'] in user_data['user_quiz_venues'] else 0
    price_score = 1 if user_data['min_price'] <= event['price'] <= user_data['max_price'] else 0
    
    # linearly weighted sum of scores
    # total_score = (genre_score * genre_weight) + (venue_score * venue_weight) + (price_score * price_weight)
    # total_score = math.log(price_score + 1) + venue_score*venue_weight + genre_score*genre_weight
    total_score = genre_score + venue_score + price_score + genre_score * venue_score
    
    return total_score


def recommend_events(events, user_data):
    """
    Recommend events based on scores calculated from user preferences.
    """
    for event in events:
        event['score'] = score_event(event, user_data)
    
    # sort events by score in descending order
    recommended_events = sorted(events, key=lambda x: x['score'], reverse=True)
    
    return recommended_events


def recommend_top_20_events(recommended_events):
    """
    Recommend top 20 events from the list of recommended events.
    """
    top_20_events = recommended_events[:20]
    top_20_events_ids = [event['event_id'] for event in top_20_events]
    
    return top_20_events_ids, top_20_events

# database connection
engine = create_engine('postgresql://postgres:system@localhost:5432/spotevent')


# user_data = import_prep_data('m.tweedy', engine)
# user_data = import_prep_data('srisky', engine)
# user_data = import_prep_data('Finn', engine)
user_data = import_prep_data('aidan959', engine)
if user_data:
    # print("user_data: ", user_data)
    print("User Data and Events loaded successfully.")
else:
    print("User data not found.")

recommended_events = recommend_events(user_data['events'], user_data)
# print recommended events
for event in recommended_events:
    print(f"Event: {event['name']} | Venue: {event['venue_name']} | (Score: {event['score']})")

top_20_events_ids, top_20_events = recommend_top_20_events(recommended_events)

# print top 20 event IDs from event list
print("Top 20 Event IDs: ", top_20_events_ids)
print("Top 20 Events:\n ", pd.DataFrame(top_20_events))