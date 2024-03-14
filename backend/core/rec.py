import ast
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TODO : test adjust_similarity_scores_venues_genres properly
# ! it is not working as expected : changing += 0.5 to -= 0.5 and vice versa does not change the output
# TODO: after 10 recommendations, check the date of the event to current date and filter out events that have already happened

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

    # begin basic recommendation system
    
    # convert the string representations of lists into actual lists
    song_data['genres'] = song_data['genres'].apply(ast.literal_eval)
    artist_data['genres'] = artist_data['genres'].apply(ast.literal_eval)
    # event_data['tags'] is already a list, so no need to convert it

    # join the elements of each list into a single string
    song_data['genres'] = song_data['genres'].apply(','.join)
    artist_data['genres'] = artist_data['genres'].apply(','.join)

    # now split user data into quiz preferences
    user_quiz_venues = user_data['venue_preferences']
    user_quiz_genres = user_data['genre_preferences']
    user_quiz_pricerange = user_data['price_range']

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

    return song_data, artist_data, event_data, user_quiz_venues, user_quiz_genres, events, min_price, max_price


def feature_extraction(song_data, artist_data, event_data, user_quiz_venues, user_quiz_genres, events):
    # create a TfidfVectorizer object
    vectorizer = TfidfVectorizer()

    # fit the TfidfVectorizer on the combined data
    vectorizer.fit(song_data['genres'].tolist() + artist_data['genres'].tolist() + event_data['tags'].tolist())

    # transform the song genres, artist genres and event tags
    song_genres_tfidf = vectorizer.transform(song_data['genres'])
    artist_genres_tfidf = vectorizer.transform(artist_data['genres'])
    event_tfidf = vectorizer.transform([event['tags'] for event in events])

    # create a user profile
    user_profile = vectorizer.transform(user_quiz_venues + user_quiz_genres)

    return user_profile, event_tfidf, song_genres_tfidf, artist_genres_tfidf

def get_similarity_scores(user_profile, event_tfidf, song_genres_tfidf, artist_genres_tfidf):
    # cosine sim between user profile and events
    user_event_similarity = cosine_similarity(user_profile, event_tfidf)

    # songs - events
    song_event_similarity = cosine_similarity(song_genres_tfidf, event_tfidf)

    # artists - events
    artist_event_similarity = cosine_similarity(artist_genres_tfidf, event_tfidf)

    return user_event_similarity, song_event_similarity, artist_event_similarity


def matrix_padding(song_event_similarity, artist_event_similarity):
    # get the maximum shape of the two similarity matrices
    max_shape = max(song_event_similarity.shape, artist_event_similarity.shape)

    # create zero matrices with the maximum shape
    song_event_similarity_padded = np.zeros(max_shape)
    artist_event_similarity_padded = np.zeros(max_shape)

    # pad the similarity matrices with zeros so they can be added together
    song_event_similarity_padded[:song_event_similarity.shape[0], :song_event_similarity.shape[1]] = song_event_similarity
    artist_event_similarity_padded[:artist_event_similarity.shape[0], :artist_event_similarity.shape[1]] = artist_event_similarity

    return song_event_similarity_padded, artist_event_similarity_padded


def adjust_similarity_scores_venues_genres(song_event_similarity_padded, artist_event_similarity_padded, user_event_similarity ,user_quiz_venues, user_quiz_genres, min_price, max_price, events):
    # calculate the average similarity between songs and events and artists and events
    average_similarity = np.mean([song_event_similarity_padded, artist_event_similarity_padded], axis=0)

    # calculate the average similarity between the user's Spotify data and the user's event preferences
    weighted_similarity = (2 * average_similarity + user_event_similarity) / 3

    # pad the weighted_similarity array with zeros if it's shorter than the events list
    if len(weighted_similarity) < len(events):
        weighted_similarity = np.pad(weighted_similarity, (0, len(events) - len(weighted_similarity)), 'constant')

    for i, event in enumerate(events):
        # initialize the adjusted_similarity score to the weighted similarity score
        event['adjusted_similarity'] = np.mean(weighted_similarity[i])

        # check if event venue is in user's preferences
        if event['venue_name'].lower() in [venue.lower() for venue in user_quiz_venues]:
            event['adjusted_similarity'] += 0

        # check if event genre is in user's preferences
        if any(tag.lower() in [genre.lower() for genre in user_quiz_genres] for tag in event['tags']):
            event['adjusted_similarity'] += 0

        # check if event price is within user's preferred range
        if min_price <= event['price'] <= max_price:
            event['adjusted_similarity'] += 0

    return events


# # get the indices of the events sorted by similarity
def get_sorted_indices(adjusted_events):
    adjusted_indices = np.argsort([event['adjusted_similarity'] for event in adjusted_events])[::-1]
    return adjusted_indices.flatten()

# get the top 10 most similar events
def get_top_events(event_data, adjusted_indices, num_events=10):
    top_events = event_data.iloc[adjusted_indices[:num_events]]
    print(top_events)
    return top_events['event_id'].tolist()


def main(username):
    # Setup database connection
    engine = setup_db_conn()

    # Import and prepare data
    song_data, artist_data, event_data, user_quiz_venues, user_quiz_genres, events, min_price, max_price = import_prep_data(username, engine)

    # Feature extraction
    user_profile, event_tfidf, song_genres_tfidf, artist_genres_tfidf = feature_extraction(song_data, artist_data, event_data, user_quiz_venues, user_quiz_genres, events)

    # Get similarity scores
    user_event_similarity, song_event_similarity, artist_event_similarity = get_similarity_scores(user_profile, event_tfidf, song_genres_tfidf, artist_genres_tfidf)

    # Matrix padding
    song_event_similarity_padded, artist_event_similarity_padded = matrix_padding(song_event_similarity, artist_event_similarity)

    # Adjust similarity scores
    adjusted_events = adjust_similarity_scores_venues_genres(song_event_similarity_padded, artist_event_similarity_padded, user_event_similarity, user_quiz_venues, user_quiz_genres, min_price, max_price, events)

    # Get sorted indices
    adjusted_indices = get_sorted_indices(adjusted_events)

    # Get top 10 events
    top_10_event_ids = get_top_events(event_data, adjusted_indices)

    return top_10_event_ids

if __name__ == "__main__":
    main('m.tweedy')
    print("Recommendations generated successfully.")