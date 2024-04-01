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
    
    # Combine all features
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
    # Filter events by top_clusters
    filtered_events = [event for event in events if event['cluster'] in top_clusters]
    
    # Continue with existing scoring and recommendation logic on filtered_events
    recommended_events = recommend_events(filtered_events, user_data, 'final_score')
    return recommended_events

# Example adjustment, adding a cluster preference score
def score_event_with_cluster_preference(event, user_data, preferred_clusters):
    base_score = score_event(event, user_data)  # Your existing scoring logic
    cluster_bonus = 0.1 if event['cluster'] in preferred_clusters else 0
    return base_score + cluster_bonus

def determine_user_preferred_clusters(user_data, events):
    # Placeholder: This logic should be replaced with your method of determining preferences
    # For demonstration, let's assume we derive the preferred clusters based on user's genre preferences
    # and looking at which clusters these genres appear most frequently

    # Example: Counting cluster appearances based on user's favorite genres
    cluster_count = {}
    for event in events:
        if any(genre in user_data['user_mapped_genres'] for genre in event['tags']):
            cluster = event['cluster']
            if cluster not in cluster_count:
                cluster_count[cluster] = 0
            cluster_count[cluster] += 1

    # Sort clusters by their count and return top N
    preferred_clusters = sorted(cluster_count, key=cluster_count.get, reverse=True)[:3]  # Adjust N based on needs
    return preferred_clusters


def calculate_spotify_preference_score(user_data, event):
    """
    Calculate a score based on user's Spotify data (preferred genres and artists).
    """
    genre_match_score = 0
    artist_match_score = 0
    
    # Assume you have a way to extract preferred artists from user_data
    preferred_artists = user_data.get('preferred_artists', [])
    
    # Genre match calculation
    if user_data['user_mapped_genres']:
        genre_match_score = calculate_genre_similarity(user_data['user_mapped_genres'], event['tags'])
    
    # Artist match calculation
    if preferred_artists and 'artist' in event:
        artist_match_score = 1 if event['artist'] in preferred_artists else 0
    
    return genre_match_score, artist_match_score
# -----------------------------------------------------------------------------------------------------------



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
    # This function uses your existing logic to calculate scores
    for event in events:
        event['score'] = score_event(event, user_data)


# def integrate_tfidf_scores(events, cosine_?similarities):
    # for i, event in enumerate(events):
        # event['tfidf_score'] = cosine_similarities[i]
        # Here, you integrate TF-IDF scores; ensure this is done before sorting based on 'tfidf_score'


def update_event_scores_with_tfidf(events, cosine_similarities):
    # Assuming original scores are biased towards user-declared preferences
    # and TF-IDF scores are biased towards content similarity,
    # and given the feedback that genre > price > venues,
    # we lean more on TF-IDF which captures content/genre similarity.
    original_score_weight = 0.9
    tfidf_score_weight = 0.1

    for i, event in enumerate(events):
        event['tfidf_score'] = cosine_similarities[i]
        existing_score = event['score']
        
        # Blend scores with adjusted weights
        event['final_score'] = (existing_score * original_score_weight) + (event['tfidf_score'] * tfidf_score_weight)


def adjust_weights_based_on_difference(original_score, tfidf_score):
    difference = abs(original_score - tfidf_score)
    
    # Define thresholds for difference that dictate the weighting strategy
    # These thresholds could be fine-tuned based on testing and feedback
    low_threshold = 0.1
    high_threshold = 0.3
    
    if difference <= low_threshold:
        # High agreement between scores, lean more on TF-IDF
        original_weight = 0.7
        tfidf_weight = 0.3
    elif difference <= high_threshold:
        # Moderate agreement, use balanced weights
        original_weight = 0.5
        tfidf_weight = 0.5
    else:
        # Low agreement, be cautious and lean more on original preferences
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

# pre k-means clustering
# def update_event_scores_with_dynamic_adjustment(events, cosine_similarities, top_15_original_ids):
#     for i, event in enumerate(events):
#         event['tfidf_score'] = cosine_similarities[i]
#         original_score = event['score']

#         # Adjust weights dynamically based on the agreement between scores
#         original_weight, tfidf_weight = adjust_weights_based_on_difference(original_score, event['tfidf_score'])

#         # Apply dynamically adjusted weights
#         event['final_score'] = (original_score * original_weight) + (event['tfidf_score'] * tfidf_weight)

#         # Ensure events not in the original top 10 are penalized to stay out of the top 10 in final scores
#         if event['event_id'] not in top_15_original_ids:
#             # This penalty could be adjusted. Here, it's a simple method to significantly lower the final score.
#             # It ensures these events don't make it to the final top 10 but are otherwise ranked according to their final score.
#             event['final_score'] *= 0.5

def update_event_scores_with_dynamic_adjustment(events, cosine_similarities, top_15_original_ids, preferred_clusters):
    # Fetch the maximum score from the initial scoring to maintain a scaling factor
    max_original_score = max(event['score'] for event in events if 'score' in event)

    for i, event in enumerate(events):
        event['tfidf_score'] = cosine_similarities[i]
        original_score = event['score']

        # Adjust weights dynamically based on the agreement between scores
        original_weight, tfidf_weight = adjust_weights_based_on_difference(original_score, event['tfidf_score'])

        # Apply dynamically adjusted weights
        event['final_score'] = (original_score * original_weight) + (event['tfidf_score'] * tfidf_weight)

        # Incorporate cluster preference in the final score
        if event['cluster'] in preferred_clusters:
            # Increase final score for preferred clusters
            event['final_score'] += max_original_score * 0.1  # 10% of the max original score as a bonus

        # Ensure events not in the original top 15 are penalized to stay out of the top 10 in final scores
        if event['event_id'] not in top_15_original_ids:
            # This penalty is applied to significantly lower the final score
            # It ensures these events don't make it to the final top 10 but are otherwise ranked according to their final score
            event['final_score'] *= 0.5  # Apply a 25% reduction to the final score of events not in the original top 15


# Ensuring the `score_event` function uses the correct key based on the context provided
def score_event(event, user_data, preferred_clusters=None):
    # Weights for various components
    genre_weight = 0.4
    price_weight = 0.2
    venue_weight = 0.1
    cluster_bonus_weight = 0.05
    spotify_genre_weight = 0.1
    spotify_artist_weight = 0.15
    
    # Calculate Spotify preference scores (genres and artists)
    genre_score, artist_score = calculate_spotify_preference_score(user_data, event)
    
    # Check if the event is in a preferred cluster
    cluster_bonus = 1 if preferred_clusters and event.get('cluster') in preferred_clusters else 0
    
    # Original genre similarity score (based on user's genre preferences and event's genres)
    original_genre_score = calculate_genre_similarity(user_data['user_mapped_genres'], event['tags'])
    
    # Calculate price score
    if 'price' in event and event['price'] is not None:
        if user_data['min_price'] <= event['price'] <= user_data['max_price']:
            price_score = 1  # Full score if within range
        else:
            # Optional: Adjust this logic to provide partial scores for close matches
            price_score = 0  # No score if outside range
    else:
        price_score = 0.5  # Neutral score if price data is missing or irrelevant

    # Calculate total score incorporating all the components
    event_score = (original_genre_score * genre_weight) + \
                  (genre_score * spotify_genre_weight) + \
                  (artist_score * spotify_artist_weight) + \
                  (price_score * price_weight) + \
                  (event.get('venue_score', 0) * venue_weight) + \
                  (cluster_bonus * cluster_bonus_weight)
    
    return event_score


# -----------------------------------------------------------------------------------------------------------


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


# def score_event(event, user_data):
#     """
#     Score an event based on user preferences, including genre similarity, venue preference, and price sensitivity.
#     """
#     genre_weight = 0.7
#     price_weight = 0.3 # Adjusted to ensure weights sum to 1
#     venue_weight = 0.3

#     genre_score = calculate_genre_similarity(user_data['user_mapped_genres'], event['tags'])
#     venue_score = 1 if event['venue_name'] in user_data['user_quiz_venues'] else 0
#     price_score = 1 if user_data['min_price'] <= event['price'] <= user_data['max_price'] else 0
    
#     # linearly weighted sum of scores
#     # total_score = (genre_score * genre_weight) + (venue_score * venue_weight) + (price_score * price_weight)
#     total_score = math.log(price_score + 1) + venue_score*venue_weight + genre_score*genre_weight
#     # total_score = genre_score + venue_score + price_score + genre_score * venue_score
    
#     return total_score


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


def recommend_top_20_events(recommended_events):
    """
    Recommend top 20 events from the list of recommended events.
    """
    top_20_events = recommended_events[:20]
    top_20_events_ids = [event['event_id'] for event in top_20_events]
    
    return top_20_events_ids, top_20_events


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

    # Prepare features and cluster events
    features = encode_and_scale_features(user_data['events'])
    clusters = cluster_events(features, n_clusters=5)  # n_clusters might be adjusted
    assign_clusters_to_events(user_data['events'], clusters)

    # Determine preferred clusters based on user data
    preferred_clusters = determine_user_preferred_clusters(user_data, user_data['events'])

    # Calculate original scores with cluster preferences considered
    for event in user_data['events']:
        event['score'] = score_event(event, user_data, preferred_clusters)

    # Retrieve the IDs of top 15 events based on the original score
    top_15_original_ids = get_top_n_event_ids(user_data['events'], 'score', 15)

    # TF-IDF model preparation and cosine similarity calculation
    user_vector, event_vectors = prepare_tfidf_model(user_data['events'], user_data['user_mapped_genres'])
    cosine_similarities = calculate_cosine_similarity(user_vector, event_vectors)

    # Assign TF-IDF scores to events and adjust final scores with dynamic weight adjustment
    # Ensuring events not in the original top 15 are appropriately ranked
    update_event_scores_with_dynamic_adjustment(user_data['events'], cosine_similarities, top_15_original_ids, preferred_clusters)

    print("Top 20 based on Original Scores:")
    print_top_20_events(user_data['events'], 'score')

    print("Top 20 based on TF-IDF Scores:")
    print_top_20_events(user_data['events'], 'tfidf_score')

    print("Top 20 based on Final Blended Scores with Cluster Preferences:")
    print_top_20_events(user_data['events'], 'final_score')

    # Sort events by final_score in descending order
    sorted_events_by_final_score = sorted(user_data['events'], key=lambda x: x.get('final_score', 0), reverse=True)
    
    # Extract the top 20 events
    top_20_events = sorted_events_by_final_score[:20]

    # Extract IDs and details of the top 20 events
    top_20_event_ids = [event['event_id'] for event in top_20_events]
    # top_20_event_details = [{ 'event_id': event['event_id'], 'name': event['name'], 'final_score': event['final_score']} for event in top_20_events]
    top_20_event_details = [{
    'event_id': event['event_id'],
    'name': event['name'],
    'final_score': event['final_score'],
    'price': event['price']  # Ensure the price is extracted here
    } for event in top_20_events]
    
    # Example: Print or return the top 20 event IDs and details
    print("Top 20 Event IDs:", top_20_event_ids)
    for event in top_20_event_details:
        print(f"ID: {event['event_id']}, Name: {event['name']}, Final Score: {event['final_score']}, Price: {event['price']}")

    # Depending on your requirements, you can return these IDs or details
    return top_20_event_ids

    # # database connection
    # engine = create_engine('postgresql://postgres:system@localhost:5432/spotevent')

    # user_data = import_prep_data(username, engine)

    # if not user_data:
    #     print("User data not found.")
    #     return
    
    # # normal weighted recommendation
    # weighted_recommended_events = recommend_events(user_data['events'], user_data, score_key='score')
    # top_20_events_ids, top_20_events = recommend_top_20_events(weighted_recommended_events)
    # print("Top 20 Event IDs: ", top_20_events_ids)
    # print("Top 20 Events:\n ", pd.DataFrame(top_20_events))
    
    # # prepare TF-IDF model
    # user_vector, event_vectors = prepare_tfidf_model(user_data['events'], user_data['user_mapped_genres'])

    # # calculate cosine similarity
    # cosine_similarities = calculate_cosine_similarity(user_vector, event_vectors)

    # # update event scores with TF-IDF cosine similarities
    # for i, event in enumerate(user_data['events']):
    #     event['tfidf_score'] = cosine_similarities[i]

    # # might want to blend TF-IDF scores with existing scores
    # # e.g average the existing score with the TF-IDF score
    # for event in user_data['events']:
    #     event['final_score'] = (event['score'] + event['tfidf_score']) / 2

    # # recommend events based on final scores
    # recommended_events = recommend_events(user_data['events'], user_data, score_key='final_score')

    # # display top 20 events
    # print("With TF-IDF:")
    # for event in recommended_events:
    #     print(f"Event: {event['name']} | (Score: {event['score']}) | (tfScore: {event['final_score']}) | (fScore: {event['final_score']})")

    # ------------------------------------------------------------------------------------------------------------------------------------
    # before TF-IDF implementation

    # user_data = import_prep_data('m.tweedy', engine)
    # user_data = import_prep_data('srisky', engine)
    # user_data = import_prep_data('Finn', engine)
    # user_data = import_prep_data('aidan959', engine)
    # if user_data:
    #     # print("user_data: ", user_data)
    #     print("User Data and Events loaded successfully.")
    # else:
    #     print("User data not found.")

    # recommended_events = recommend_events(user_data['events'], user_data)
    # # print recommended events
    # for event in recommended_events:
    #     print(f"Event: {event['name']} | Venue: {event['venue_name']} | (Score: {event['score']})")

    # top_20_events_ids, top_20_events = recommend_top_20_events(recommended_events)

    # # print top 20 event IDs from event list
    # print("Top 20 Event IDs: ", top_20_events_ids)
    # print("Top 20 Events:\n ", pd.DataFrame(top_20_events))
        
if __name__ == '__main__':
    main('m.tweedy')