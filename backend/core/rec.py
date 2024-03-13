import ast
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TODO : test adjust_similarity_scores_venues_genres properly
# ! it is not working as expected : changing += 0.5 to -= 0.5 and vice versa does not change the output
# TODO: after 10 recommendations, check the date of the event to current date and filter out events that have already happened

username = 'm.tweedy' # have this passed in from the frontend

# create a connection to the PostgreSQL database
engine = create_engine('postgresql://postgres:system@localhost:5432/spotevent')

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
# Step 1 : DATA PREPARATION ---------------------------------------------------------------

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

# Step 2 : FEATURE EXTRACTION -----------------------------------------------------------
# create a TfidfVectorizer object
vectorizer = TfidfVectorizer()

# fit the TfidfVectorizer on the combined data
vectorizer.fit(song_data['genres'].tolist() + event_data['tags'].tolist())
vectorizer.fit(artist_data['genres'].tolist() + event_data['tags'].tolist())

# transform the song genres and event tags
song_genres_tfidf = vectorizer.transform(song_data['genres'])
artist_genres_tfidf = vectorizer.transform(artist_data['genres'])
# event_tags_tfidf = vectorizer.transform(event_data['tags'])
event_tfidf = vectorizer.transform([event['tags'] for event in events])

similarity_scores = cosine_similarity(song_genres_tfidf, event_tfidf)

for i, event in enumerate(events):
    event['similarity'] = similarity_scores[0][i]

# create a user profile
user_profile = vectorizer.transform(user_quiz_venues + user_quiz_genres)

# Step 3 : COSINE SIMILARITY -------------------------------------------------------------
# calculate the cosine similarity

# cosine sim between user profile and events
# user_event_similarity = cosine_similarity(user_profile, event_tags_tfidf)
user_event_similarity = cosine_similarity(user_profile, event_tfidf)

# songs - events
# song_event_similarity = cosine_similarity(song_genres_tfidf, event_tags_tfidf)
song_event_similarity = cosine_similarity(song_genres_tfidf, event_tfidf)

# artists - events
# artist_event_similarity = cosine_similarity(artist_genres_tfidf, event_tags_tfidf)
artist_event_similarity = cosine_similarity(artist_genres_tfidf, event_tfidf)

print(song_event_similarity)
print(artist_event_similarity)
print("USER-EVENT SIM", user_event_similarity)


# Step 4 : RECOMMENDATION ----------------------------------------------------------------

# get the maximum shape of the two similarity matrices
max_shape = max(song_event_similarity.shape, artist_event_similarity.shape)

# create zero matrices with the maximum shape
song_event_similarity_padded = np.zeros(max_shape)
artist_event_similarity_padded = np.zeros(max_shape)

# pad the similarity matrices with zeros so they can be added together
song_event_similarity_padded[:song_event_similarity.shape[0], :song_event_similarity.shape[1]] = song_event_similarity
artist_event_similarity_padded[:artist_event_similarity.shape[0], :artist_event_similarity.shape[1]] = artist_event_similarity

# ____________________________ MAYBE NOT RELEVANT ____________________________

def adjust_similarity_scores_venues_genres(user_quiz_venues, user_quiz_genres, min_price, max_price, events):
    for event in events:
        # calculate the average similarity between songs and events and artists and events
        average_similarity = np.mean([song_event_similarity_padded, artist_event_similarity_padded], axis=0)

        # calculate the average similarity between the user's Spotify data and the user's event preferences
        weighted_similarity = (2 * average_similarity + user_event_similarity) / 3

        # initialize the adjusted_similarity score to the weighted similarity score
        event['adjusted_similarity'] = weighted_similarity

        # check if event venue is in user's preferences
        if event['venue_name'].lower() in [venue.lower() for venue in user_quiz_venues]:
            event['adjusted_similarity'] += 0.3

        # check if event genre is in user's preferences
        if any(tag.lower() in [genre.lower() for genre in user_quiz_genres] for tag in event['tags']):
            event['adjusted_similarity'] += 0.5

        # check if event price is within user's preferred range
        if min_price <= event['price'] <= max_price:
            event['adjusted_similarity'] += 0.075

    return events

# ____________________________ MAYBE NOT RELEVANT ____________________________

# get the indices of the events sorted by similarity
adjusted_events = adjust_similarity_scores_venues_genres(user_quiz_venues, user_quiz_genres, min_price, max_price, events)

# get the indices of the events sorted by similarity
# average_indices = average_similarity.argsort()[:, ::-1]
adjusted_indices = np.argsort([event['adjusted_similarity'] for event in adjusted_events])[::-1]

adjusted_indices = adjusted_indices.flatten()

# get the top 10 most similar events
top_10_events = event_data.iloc[adjusted_indices[:10]]

print(top_10_events)