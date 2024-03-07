import ast
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

print(song_data.head())
print(artist_data.head())

# print(song_data['genres'][0][0]) # prints the first genre of the first song

song_data.info()
artist_data.info()

# show theres no missing data
song_data.dropna(inplace=True)
song_data.isnull().sum().plot.bar()
plt.show()

artist_data.dropna(inplace=True)
artist_data.isnull().sum().plot.bar()
plt.show()

# load remaining data into pandas DataFrames
event_data = pd.read_sql('SELECT * FROM backend_event', engine)
venue_data = pd.read_sql('SELECT * FROM backend_venue', engine)

print(event_data.head())
print(venue_data.head())
print(event_data['tags'].head())


# ------------------------ MAYBE NOT RELEVANT ------------------------
# combines all the data into a single list
# create a list of all genres
genres = []
for i in range(len(song_data)):
    for j in range(len(song_data['genres'][i])):
        if song_data['genres'][i] not in genres:
            genres.append(song_data['genres'][i])

# create a list of all artists
artists = []
for i in range(len(artist_data)):
    artists.append(artist_data['name'][i])

# create a list of all venues
venues = []
for i in range(len(venue_data)):
    venues.append(venue_data['name'][i])

# create a list of all events
events = []
for i in range(len(event_data)):
    events.append(event_data['name'][i])

# create a list of all tags
tags = []
for i in range(len(event_data)):
    tags.append(event_data['tags'][i])

# create a list of all songs
songs = []
for i in range(len(song_data)):
    songs.append(song_data['name'][i])

print(f"{songs = }")
print(f"{artists = }")
print(f"{events = }")
print(f"{venues = }")
print(f"{tags = }")
print(f"{genres = }")
# ------------------------ MAYBE NOT RELEVANT ------------------------

# begin basic recommendation system
# Step 1 : DATA PREPARATION ---------------------------------------------------------------

# convert the string representations of lists into actual lists
song_data['genres'] = song_data['genres'].apply(ast.literal_eval)
artist_data['genres'] = artist_data['genres'].apply(ast.literal_eval)
# event_data['tags'] is already a list, so no need to convert it

# join the elements of each list into a single string
song_data['genres'] = song_data['genres'].apply(','.join)
artist_data['genres'] = artist_data['genres'].apply(','.join)

print(song_data['genres'].head())
print(artist_data['genres'].head())
print(event_data['tags'].head())

# Step 2 : FEATURE EXTRACTION -----------------------------------------------------------
# create a TfidfVectorizer object
vectorizer = TfidfVectorizer()

# fit the TfidfVectorizer on the combined data
vectorizer.fit(song_data['genres'].tolist() + event_data['tags'].tolist())
vectorizer.fit(artist_data['genres'].tolist() + event_data['tags'].tolist())

# transform the song genres and event tags
song_genres_tfidf = vectorizer.transform(song_data['genres'])
artist_genres_tfidf = vectorizer.transform(artist_data['genres'])
event_tags_tfidf = vectorizer.transform(event_data['tags'])

# Step 3 : COSINE SIMILARITY -------------------------------------------------------------
# calculate the cosine similarity

# songs - events
song_event_similarity = cosine_similarity(song_genres_tfidf, event_tags_tfidf)

# artists - events
artist_event_similarity = cosine_similarity(artist_genres_tfidf, event_tags_tfidf)

print(song_event_similarity)
print(artist_event_similarity)

# create a heatmap from the cosine similarity matrix
plt.figure(figsize=(5, 4))
sns.heatmap(song_event_similarity, cmap='coolwarm')
plt.title('Cosine Similarity Between Songs and Events')
plt.show()

plt.figure(figsize=(5, 4))
sns.heatmap(artist_event_similarity, cmap='coolwarm')
plt.title('Cosine Similarity Between Artists and Events')
plt.show()

# Step 4 : RECOMMENDATION ----------------------------------------------------------------

# get the maximum shape of the two similarity matrices
max_shape = max(song_event_similarity.shape, artist_event_similarity.shape)

# create zero matrices with the maximum shape
song_event_similarity_padded = np.zeros(max_shape)
artist_event_similarity_padded = np.zeros(max_shape)

# pad the similarity matrices with zeros so they can be added together
song_event_similarity_padded[:song_event_similarity.shape[0], :song_event_similarity.shape[1]] = song_event_similarity
artist_event_similarity_padded[:artist_event_similarity.shape[0], :artist_event_similarity.shape[1]] = artist_event_similarity

# calculate the average similarity between songs and events and artists and events
average_similarity = np.mean([song_event_similarity_padded, artist_event_similarity_padded], axis=0)

# get the indices of the events sorted by similarity
average_indices = average_similarity.argsort()[:, ::-1]

# get the top 10 most similar events
top_10_events = event_data.iloc[average_indices[0][:10]]

print(top_10_events)