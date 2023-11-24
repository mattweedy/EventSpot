import pandas as pd
import numpy as np
import json
import re 
import sys
import itertools

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

import warnings
warnings.filterwarnings("ignore")

#another useful command to make data exploration easier
# NOTE: if you are using a massive dataset, this could slow down your code. 
# pd.set_option('display.max_columns', None)
# pd.set_option("max_rows", None)

pd.options.display.max_columns = 0
pd.options.display.max_rows = 0

# TODO: methods to handle json strings ---

# data exploration/prep
with open('data/users.json') as json_users_data:
    users = json.load(json_users_data)

user_df = pd.DataFrame(users["objects"])
user_df.head()
user_df.dtypes

# display first user's fav genre
print(user_df['user_fav_genre'].values[0])
# "Jazz"
print(user_df['user_fav_song'].values[0])
# "Candyman"
print(user_df['user_fav_genre'].values[0][0])
# "J"

# if im using multiple genres per users, this will extract and add them into a separate list
user_df['fav_genre_upd'] = user_df['user_fav_genre'].apply(lambda x: [re.sub(' ','_',i) for i in re.findall(r"'(^'*)'", x)])
print(user_df['fav_genre_upd'].values[0])
# []
# ----------------------------------------