import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine

# Create a connection to the PostgreSQL database
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# Load your data into pandas DataFrames
# For simplicity, let's assume you have two tables: user_data and event_data
user_data = pd.read_sql('SELECT * FROM user_data', engine)
event_data = pd.read_sql('SELECT * FROM event_data', engine)

# Extract the features
# In this case, let's assume the 'genres' column contains the genres of the user's top songs and artists, and the events
user_genres = user_data['genres']
event_genres = event_data['genres']

# Vectorize the genres using TF-IDF
vectorizer = TfidfVectorizer()
user_genres_vectorized = vectorizer.fit_transform(user_genres)
event_genres_vectorized = vectorizer.transform(event_genres)

# Calculate the cosine similarity between the user's preferences and the events
similarity_scores = cosine_similarity(user_genres_vectorized, event_genres_vectorized)

# Generate recommendations
# For each user, recommend the top 5 events with the highest similarity scores
recommendations = {}
for i in range(similarity_scores.shape[0]):
    top_5_indices = similarity_scores[i].argsort()[-5:][::-1]
    recommendations[user_data.loc[i, 'user_id']] = event_data.loc[top_5_indices, 'event_id'].values

# Print the recommendations to the console
for user_id, event_ids in recommendations.items():
    print(f'Recommendations for user {user_id}: {event_ids}')