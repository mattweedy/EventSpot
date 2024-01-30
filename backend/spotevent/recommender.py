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

# print(users_df.head(15))
# print(events_df.head(15))

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

# print(user_songs)
# print(events)

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
    # Create a combined genre string for the input genre
    combined_genre = ' '.join([eventGenre]*4)

    # Vectorize the combined genre string
    combined_genre_cv = cv.transform([combined_genre])

    # Calculate cosine similarity with all events
    sim_scores = cosine_similarity(combined_genre_cv, events_cv).flatten()

    # Get the indexes of the events sorted by similarity
    sorted_indexes = np.argsort(sim_scores)[::-1]

    # Get the top N most similar events
    top_n = 5
    recommended_events = events_df.iloc[sorted_indexes[:top_n]]

    return recommended_events

# print(event_recommender('Soul'))
# print(event_recommender('Techno'))

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