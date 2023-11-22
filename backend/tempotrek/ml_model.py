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

# data exploration/prep
user_df = pd.read_json('/data/ExportJson-users.json')
user_df.head()
user_df.dtypes

# display first user's fav genre
user_df['user_fav_genre'].values[0]