import numpy as np
import pandas as pd
import tweepy
from tweepy import Cursor
from keys import api_key, api_secret_key
import json

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

classifier = SentimentIntensityAnalyzer()

auth = tweepy.OAuthHandler(api_key, api_secret_key)
api = tweepy.API(auth)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def twitter_search(search):
    df_list = []
    for tweet in Cursor(api.search, q=search, tweet_mode="extended").items(1000):
        temp_dict = {}
        temp_dict['id'] = tweet.id_str
        temp_dict['created_at'] = tweet.created_at
        temp_dict['full_text'] = tweet.full_text
        temp_dict['retweet_count'] = tweet.retweet_count
        df_list.append(temp_dict)
    df = pd.DataFrame.from_dict(df_list)

    def classify(text):
        scores = classifier.polarity_scores(text)
        del scores['compound']
        label = max(scores, key=scores.get)
        score = scores[label]
        return label, score

    df['label'], df['score'] = zip(*df['full_text'].map(lambda x: classify(x)))

    df['date'] = df['created_at'].apply(lambda x: x.date())

    total = len(df)
    total_pos = len(df[df['label'] == 'pos'])
    total_neg = len(df[df['label'] == 'neg'])
    total_neu = len(df[df['label'] == 'neu'])

    try:
        idx_max_pos = df[df['label'] == 'pos']['score'].idxmax()
    except: pass
    try:
        idx_max_neg = df[df['label'] == 'neg']['score'].idxmax()
    except: pass
    try:
        idx_max_retweets = df['retweet_count'].idxmax()
    except: pass
    
    try:
        id_max_pos = df.iloc[idx_max_pos]['id']
    except: id_max_pos = None
    try:
        id_max_neg = df.iloc[idx_max_neg]['id']
    except: id_max_neg = None
    try:
        id_max_retweets = df.iloc[idx_max_retweets]['id']
    except: id_max_retweets = None
    try:
        full_text_pos = df.iloc[idx_max_pos]['full_text']
    except: full_text_pos = "No positive tweets!"
    try:
        full_text_neg = df.iloc[idx_max_neg]['full_text']
    except: full_text_neg = "No negative tweets!"
    try:
        full_text_retweets = df.iloc[idx_max_retweets]['full_text']
    except: full_text_retweets = "No tweets were retweeted!"

    dates = df.groupby('date').count().reset_index()['date']
    dates = list(dates.apply(lambda x: x.strftime("%d/%m/%Y")))
    tweets_per_day = list(df.groupby('date').count().reset_index()['id'])

    line_df = df.groupby(['date', 'label']).count().reset_index()

    line_df = line_df.pivot(index='date', columns='label', values='id').reset_index()

    if total_pos == 0:
        line_df['pos'] = 0
    if total_neg == 0:
        line_df['neg'] = 0
    if total_neu == 0:
        line_df['neu'] = 0
        
    line_df = line_df.fillna(0)
    
    def f(row):
        val = 100 * (row['pos'] + row['neu']) / (row['pos'] + (row['neg']) + (row['neu']))
        return round(val)

    pos_tweets_per_day = list(line_df.apply(f, axis=1))


    dict_data = {
        'totals': {
            'total': total,
            'total_pos': total_pos,
            'total_neg': total_neg,
            'total_neu': total_neu
            },
        'line': {
            'dates': dates,
            'pos_tweets_per_day': pos_tweets_per_day
            },
        'bar': {
            'dates': dates,
            'tweets_per_day': tweets_per_day
            },
        'tweets': {
            'id_max_pos': id_max_pos,
            'id_max_neg': id_max_neg,
            'id_max_retweets': id_max_retweets,
            'full_text_pos': full_text_pos,
            'full_text_neg': full_text_neg,
            'full_text_retweets': full_text_retweets
            }
        }



    json_data = json.dumps(dict_data, cls=NpEncoder)

    return json_data