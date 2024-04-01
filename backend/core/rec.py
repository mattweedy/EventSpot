import ast
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, MinMaxScaler

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
        
        combined_genres = user_song_genres + user_artist_genres
        user_mapped_genres = map_user_genres(combined_genres, genre_dict)

        if 'user_mapped_genres' not in user_data.columns:
            user_data['user_mapped_genres'] = pd.Series(dtype='object')  # Ensure column exists
        user_data.at[0, 'user_mapped_genres'] = user_mapped_genres  # Correctly setting the value

        preferred_artists = artist_data  # Extract or define this list based on user's Spotify data
        if 'preferred_artists' not in user_data.columns:
            user_data['preferred_artists'] = pd.Series(dtype='object')
        user_data.at[0, 'preferred_artists'] = preferred_artists

        # user_data['user_mapped_genres'] = user_mapped_genres

        # combined_genres = user_song_genres + user_artist_genres + user_quiz_genres
        # user_mapped_genres = map_user_genres(combined_genres, genre_dict)
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


# -----------------------------------------------------------------------------------------------------------
# TF-IDF

def prepare_tfidf_model(events, user_mapped_genres):
    # combine event tags and user genres into one list for TF-IDF
    all_genres = [' '.join(event['tags']) for event in events] + [' '.join(user_mapped_genres)]

    # create a TF-IDF vectorizer and fit_transform it to all genres
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_genres)

    # separate user vector from event vectors
    user_vector = tfidf_matrix[-1]
    event_vectors = tfidf_matrix[:-1]
    # print("user_vector: ", user_vector)
    # print("event_vectors: ", event_vectors)

    return user_vector, event_vectors

def calculate_cosine_similarity(user_vector, event_vectors):
    # calc cosine similarity between user vector and event vectors
    similarities = cosine_similarity(user_vector, event_vectors)[0]
    # print("similarities: ", similarities)

    return similarities


def calculate_original_scores(events, user_data):
    for event in events:
        event['score'] = score_event(event, user_data)


def update_event_scores_with_tfidf(events, cosine_similarities):
    # original scores are biased towards user-declared preferences
    # and TF-IDF scores are biased towards content similarity,
    # and given the feedback that genre > price > venues,
    # choosing to lean less on TF-IDF
    original_score_weight = 0.9
    tfidf_score_weight = 0.1

    for i, event in enumerate(events):
        event['tfidf_score'] = cosine_similarities[i]
        existing_score = event['score']
        
        # blend scores with adjusted weights
        event['final_score'] = (existing_score * original_score_weight) + (event['tfidf_score'] * tfidf_score_weight)


def adjust_weights_based_on_difference(original_score, tfidf_score):
    difference = abs(original_score - tfidf_score)
    
    # fine-tune these thresholds based on feedback and testing
    low_threshold = 0.1
    high_threshold = 0.3
    
    if difference <= low_threshold:
        # high agreement between scores, lean more on og weights
        original_weight = 0.7
        tfidf_weight = 0.3
    elif difference <= high_threshold:
        # moderate agreement, using equal weights
        original_weight = 0.5
        tfidf_weight = 0.5
    else:
        # low agreement, lean more on original preferences still
        original_weight = 0.9
        tfidf_weight = 0.1
    
    return original_weight, tfidf_weight


def get_top_n_event_ids(events, score_key, n=15):
    """
    Returns the IDs of the top N events based on a given score key.
    """
    sorted_events = sorted(events, key=lambda x: x.get(score_key, 0), reverse=True)
    top_n_ids = [event['event_id'] for event in sorted_events[:n]]
    return set(top_n_ids)


def update_event_scores_with_dynamic_adjustment(events, cosine_similarities, top_15_original_ids, preferred_clusters):
    # fetch the maximum score from the initial scoring to maintain a scaling factor
    max_original_score = max(event['score'] for event in events if 'score' in event)

    for i, event in enumerate(events):
        event['tfidf_score'] = cosine_similarities[i]
        original_score = event['score']

        # adjust weights dynamically based on agreement between diff scores
        original_weight, tfidf_weight = adjust_weights_based_on_difference(original_score, event['tfidf_score'])

        # apply dynamically adjusted weights
        event['final_score'] = (original_score * original_weight) + (event['tfidf_score'] * tfidf_weight)

        # use cluster preference in final score
        if event['cluster'] in preferred_clusters:
            # increase final score for preferred clusters
            event['final_score'] += max_original_score * 0.1  # 10% of max og score as a bonus

        # ensure events not in the original top 15 are penalized to stay out of the top 10 in final scores
            # dont want events to be able to jump up ranks because of TF-IDF if they sohuoldnt be there
        if event['event_id'] not in top_15_original_ids:
            # ensure these events don't make it to the final top 10 but are otherwise ranked according to their final score
            event['final_score'] *= 0.5  # apply 50% reduction to final score of events not in the original top 15


def score_event(event, user_data, preferred_clusters=None):
    # weights
    genre_weight = 0.4
    price_weight = 0.2
    venue_weight = 0.1
    cluster_bonus_weight = 0.05
    spotify_genre_weight = 0.1
    spotify_artist_weight = 0.15
    
    # calc Spotify pref scores (genres and artists)
    genre_score, artist_score = calculate_spotify_preference_score(user_data, event)
    
    # check if the event is in a preferred cluster
    cluster_bonus = 1 if preferred_clusters and event.get('cluster') in preferred_clusters else 0
    
    # og genre similarity score (based on user's genre preferences and event's genres)
    original_genre_score = calculate_genre_similarity(user_data['user_mapped_genres'], event['tags'])
    
    # calc price score
    if 'price' in event and event['price'] is not None:
        if user_data['min_price'] <= event['price'] <= user_data['max_price']:
            price_score = 1  # full score if within range
        else:
            # Optional: Adjust this logic to provide partial scores for close matches
            price_score = 0.2  # No score if outside range
    else:
        price_score = 0.5  # neutral score if price data is missing or irrelevant

    # calculate total score w/ all components
    event_score = (original_genre_score * genre_weight) + \
                  (genre_score * spotify_genre_weight) + \
                  (artist_score * spotify_artist_weight) + \
                  (price_score * price_weight) + \
                  (event.get('venue_score', 0) * venue_weight) + \
                  (cluster_bonus * cluster_bonus_weight)
    
    return event_score


# -----------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------
# K-means clustering

def encode_and_scale_features(events):
    # MultiLabelBinarizer for genres and venues
    genres_mlb = MultiLabelBinarizer()
    venues_mlb = MultiLabelBinarizer()

    all_genres = [event['tags'] for event in events]
    all_venues = [[event['venue_name']] for event in events]
    
    genres_encoded = genres_mlb.fit_transform(all_genres)
    venues_encoded = venues_mlb.fit_transform(all_venues)

    # MinMaxScaler for price range (assuming price is a single value per event)
    scaler = MinMaxScaler()
    prices = np.array([[event['price']] for event in events]).reshape(-1, 1)
    prices_scaled = scaler.fit_transform(prices)
    
    # combine all features
    features = np.hstack((genres_encoded, venues_encoded, prices_scaled))
    
    return features

def cluster_events(features, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    clusters = kmeans.fit_predict(features)
    return clusters

def assign_clusters_to_events(events, clusters):
    for event, cluster in zip(events, clusters):
        event['cluster'] = cluster

def recommend_events_based_on_clusters(events, user_data, top_clusters):
    # filter events by top_clusters
    filtered_events = [event for event in events if event['cluster'] in top_clusters]
    
    # continue with existing scoring and recommendation logic on filtered_events
    recommended_events = recommend_events(filtered_events, user_data, 'final_score')
    return recommended_events

def score_event_with_cluster_preference(event, user_data, preferred_clusters):
    base_score = score_event(event, user_data)
    cluster_bonus = 0.1 if event['cluster'] in preferred_clusters else 0
    return base_score + cluster_bonus

def determine_user_preferred_clusters(user_data, events):
    # maybe improve this logic

    # count the occurrences of each cluster for events matching user's genres
    cluster_count = {}
    for event in events:
        if any(genre in user_data['user_mapped_genres'] for genre in event['tags']):
            cluster = event['cluster']
            if cluster not in cluster_count:
                cluster_count[cluster] = 0
            cluster_count[cluster] += 1

    # sort clusters by their count and return top N
    preferred_clusters = sorted(cluster_count, key=cluster_count.get, reverse=True)[:3] # try diff n values
    return preferred_clusters


def calculate_spotify_preference_score(user_data, event):
    """
    Calculate a score based on user's Spotify data (preferred genres and artists).
    """
    genre_match_score = 0
    artist_match_score = 0
    
    preferred_artists = user_data.get('preferred_artists', [])
    
    # genre match calculation
    if user_data['user_mapped_genres']:
        genre_match_score = calculate_genre_similarity(user_data['user_mapped_genres'], event['tags'])
    
    # artist match calculation
    if preferred_artists and 'artist' in event:
        artist_match_score = 1 if event['artist'] in preferred_artists else 0
    
    return genre_match_score, artist_match_score
# -----------------------------------------------------------------------------------------------------------


def recommend_events(events, user_data, score_key):
    """
    Recommend events based on scores calculated from user preferences.
    """
    if score_key == 'final_score':
        for event in events:
            event['final_score'] = score_event(event, user_data)

    if score_key == 'score':
        for event in events:
            event['score'] = score_event(event, user_data)
    
    # sort events by score in descending order
    recommended_events = sorted(events, key=lambda x: x['score'], reverse=True)
    
    return recommended_events


def print_top_20_events(events, score_type='score'):
    sorted_events = sorted(events, key=lambda x: x.get(score_type, 0), reverse=True)
    print(f"Top 20 Events based on {score_type.capitalize()} Score:")
    for event in sorted_events[:40]:
        print(f"Event: {event['name']} | {score_type.capitalize()} Score: {event.get(score_type, 'N/A')}")
    print("\n")


def main(username):
    engine = create_engine('postgresql://postgres:system@localhost:5432/spotevent')
    user_data = import_prep_data(username, engine)
    if not user_data:
        print("User data not found.")
        return

    # prep features and cluster events
    features = encode_and_scale_features(user_data['events'])
    clusters = cluster_events(features, n_clusters=5)  # n_clusters might be adjusted
    assign_clusters_to_events(user_data['events'], clusters)

    preferred_clusters = determine_user_preferred_clusters(user_data, user_data['events'])

    # calculate og scores with cluster preferences considered
    for event in user_data['events']:
        event['score'] = score_event(event, user_data, preferred_clusters)

    # retrieve IDs of top 15 events based on og score
    top_15_original_ids = get_top_n_event_ids(user_data['events'], 'score', 15)

    # TF-IDF model prep and cosine similarity calc
    user_vector, event_vectors = prepare_tfidf_model(user_data['events'], user_data['user_mapped_genres'])
    cosine_similarities = calculate_cosine_similarity(user_vector, event_vectors)

    # assign TF-IDF scores to events and adjust final scores with dynamic weight adjustment
    # ensuring events not in the original top 15 are appropriately ranked
    update_event_scores_with_dynamic_adjustment(user_data['events'], cosine_similarities, top_15_original_ids, preferred_clusters)

    # prints for debugging and testing
    print("Top 20 based on Original Scores:")
    print_top_20_events(user_data['events'], 'score')

    print("Top 20 based on TF-IDF Scores:")
    print_top_20_events(user_data['events'], 'tfidf_score')

    print("Top 20 based on Final Blended Scores with Cluster Preferences:")
    print_top_20_events(user_data['events'], 'final_score')

    # sort events in desc order of final score
    sorted_events_by_final_score = sorted(user_data['events'], key=lambda x: x.get('final_score', 0), reverse=True)
    
    top_20_events = sorted_events_by_final_score[:20]

    top_20_event_ids = [event['event_id'] for event in top_20_events]
    top_20_event_details = [{
    'event_id': event['event_id'],
    'name': event['name'],
    'final_score': event['final_score'],
    'price': event['price']
    } for event in top_20_events]
    
    print("Top 20 Event IDs:", top_20_event_ids)
    for event in top_20_event_details:
        print(f"ID: {event['event_id']}, Price: {event['price']}, Name: {event['name']}, Final Score: {event['final_score']}")

    return top_20_event_ids


if __name__ == '__main__':
    main('m.tweedy')