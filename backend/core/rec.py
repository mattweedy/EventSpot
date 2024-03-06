import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

# create a connection to the PostgreSQL database
engine = create_engine('postgresql://postgres:system@localhost:5432/spotevent')

# Load data into pandas DataFrames
artist_data = pd.read_sql('SELECT * FROM backend_artist', engine)
event_data = pd.read_sql('SELECT * FROM backend_event', engine)
venue_data = pd.read_sql('SELECT * FROM backend_venue', engine)
track_data = pd.read_sql('SELECT * FROM backend_track', engine)
# user_data = pd.read_sql('SELECT * FROM backend_user', engine)

# extract the features
# user_genres = user_data['genres']
track_genres = track_data['genres']
event_genres = event_data['genres']

# vectorize the genres using TF-IDF
vectorizer = TfidfVectorizer()
# user_genres_vectorized = vectorizer.fit_transform(user_genres)
event_genres_vectorized = vectorizer.transform(event_genres)

# calculate the cosine similarity between the user's preferences and the events
# similarity_scores = cosine_similarity(user_genres_vectorized, event_genres_vectorized)

# generate recommendations
# for each user, recommend the top 5 events with the highest similarity scores
recommendations = {}
for i in range(similarity_scores.shape[0]):
    top_5_indices = similarity_scores[i].argsort()[-5:][::-1]
    recommendations[user_data.loc[i, 'user_id']] = event_data.loc[top_5_indices, 'event_id'].values

# print recommendations to the console
for user_id, event_ids in recommendations.items():
    print(f'Recommendations for user {user_id}: {event_ids}')