import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# data_imports = ['data/users.json', 'data/events.json']
data_imports = ['/SpotEvent/backend/spotevent/data/users.json', '/SpotEvent/backend/spotevent/data/events.json']

# open and read json files
with open(data_imports[0]) as users_data:
    users_json = json.load(users_data)

with open(data_imports[1]) as events_data:
    events_json = json.load(events_data)

users_df = pd.DataFrame(users_json["objects"])
events_df = pd.DataFrame(events_json["objects"])

# extracting necessary info from data
users_features = ['user_fav_genre', 'user_fav_artist', 'user_fav_song']
events_features = ['event_name', 'event_location', 'event_genre', 'date']

# make new dataframe with only the wanted features
user_songs = users_df[users_features].copy()
events = events_df[events_features].copy()

# combine datasets
# creates a new column in  user_songs, combined_songs
# adding these columns together with a space in between each
# could be used later to match users with events based on music preferences
user_songs.loc[:, 'combined_songs'] = user_songs['user_fav_genre'] + ' ' + user_songs['user_fav_artist'] + ' ' + user_songs['user_fav_song']
events.loc[:, 'combined_events'] = events['event_name'] + ' ' + events['event_location'] + ' ' + events['event_genre'] + ' ' + events['date']

# creating countvectorizer
cv = CountVectorizer()

# vectorize each dataframe
songs_cv = cv.fit_transform(user_songs['combined_songs'])
events_cv = cv.fit_transform(events['combined_events'])

# calculate cosine similarity vector of each item in data
songs_sim = cosine_similarity(songs_cv)
events_sim = cosine_similarity(events_cv)

# event recommender - based on event genre
def event_recommender(eventGenre):
    # create a combined genre string for the input genre
    combined_genre = ' '.join([eventGenre]*4)

    # vectorize the combined genre string
    combined_genre_cv = cv.transform([combined_genre])

    # calculate cosine similarity with all events
    sim_scores = cosine_similarity(combined_genre_cv, events_cv).flatten()

    # get the indexes of the events sorted by similarity
    sorted_indexes = np.argsort(sim_scores)[::-1]

    # get the top N most similar events
    top_n = 5
    recommended_events = events_df.iloc[sorted_indexes[:top_n]]

    return recommended_events

# event recommender, taking user's favourite genre
def user_genre_recommender(userID):
    user = users_df.loc[users_df['ID'] == str(userID)].iloc[0]

    fav_genre = user['user_fav_genre']
    print(f"user[{userID}]'s name : {user['user_name']}")
    print(f"user[{userID}]'s fav genre : {fav_genre}")
    recommended_events = event_recommender(fav_genre)

    return recommended_events

while True:
    userid = input("user id to generate recommended events : ")
    print(user_genre_recommender(userid))

# cutting all old parts of rec.py to here for now:
import ast
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
    # flatten data array to only include the score


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


def calculate_genre_similarity(user_genres, event_genres):
    """
    calculate the similarity score based on matching genres.
    
    parameters:
    - user_genres (list of str): The genres the user prefers.
    - event_genres (list of str): The genres associated with the event.
    
    returns:
    - float: A similarity score between 0 and 1.
    """
    # Calculate the intersection of user and event genres
    matching_genres = set(user_genres).intersection(set(event_genres))
    # Calculate the total number of unique genres considered
    total_genres = set(user_genres).union(set(event_genres))
    
    # Calculate the similarity score as the ratio of matching genres to total genres
    similarity_score = len(matching_genres) / len(total_genres) if total_genres else 0
    return similarity_score


def adjust_similarity_scores_venues_genres(song_event_similarity_padded, artist_event_similarity_padded, user_event_similarity ,user_quiz_venues, user_quiz_genres, min_price, max_price, events):
    # calculate the average similarity between songs and events and artists and events
    average_similarity = np.mean([song_event_similarity_padded, artist_event_similarity_padded], axis=0)

    # calculate the average similarity between the user's Spotify data and the user's event preferences
    weighted_similarity = (2 * average_similarity + user_event_similarity) / 3

    # pad the weighted_similarity array with zeros if it's shorter than the events list
    if len(weighted_similarity) < len(events):
        weighted_similarity = np.pad(weighted_similarity, (0, len(events) - len(weighted_similarity)), 'constant')

    # consider this as the ideal price
    ideal_price = (min_price + max_price) / 2

    for i, event in enumerate(events):
        # initialize the adjusted_similarity score to the weighted similarity score
        event['adjusted_similarity'] = np.mean(weighted_similarity[i])

        # # check if event venue is in user's preferences
        # if event['venue_name'].lower() in [venue.lower() for venue in user_quiz_venues]:
        #     event['adjusted_similarity'] += 0.5

        # check if event venue is in user's preferences
        venue_name_lower = event['venue_name'].lower()
        if venue_name_lower in [venue.lower() for venue in user_quiz_venues]:
            event['adjusted_similarity'] += 1.0

        # # check if event genre is in user's preferences
        # if any(tag.lower() in [genre.lower() for genre in user_quiz_genres] for tag in event['tags']):
        #     event['adjusted_similarity'] += 0.5
        
        # calculate genre similarity score
        genre_similarity = calculate_genre_similarity(user_quiz_genres, event['tags'])
        # adjust similarity score based on genre similarity
        event['adjusted_similarity'] += genre_similarity * 0.9 # consider scale of adjustment based on scoring system
        
        # # check if event price is within user's preferred range
        # if min_price <= event['price'] <= max_price:
        #     event['adjusted_similarity'] += 0.2

        # calculate price similarity score
        if min_price <= event['price'] <= max_price:
            event['adjusted_similarity'] += 0.5

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