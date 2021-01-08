import numpy as np
import pandas as pd

import tweepy
from tweepy import Cursor
from keys import api_key, api_secret_key

from transformers import pipeline

import json

def twitter_search(search):
    classifier = pipeline('sentiment-analysis')


    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    api = tweepy.API(auth)


    df_list = []
    for tweet in Cursor(api.search, q=search, tweet_mode="extended").items(1000):
        temp_dict = {}
        temp_dict['id'] = tweet.id
        temp_dict['created_at'] = tweet.created_at
        temp_dict['full_text'] = tweet.full_text
        temp_dict['retweet_count'] = tweet.retweet_count
        df_list.append(temp_dict)
    df = pd.DataFrame.from_dict(df_list)

    def classify(text):
        clf = classifier(text)
        return (clf[0]['label'], clf[0]['score'])

    df['label'], df['score'] = zip(*df['full_text'].map(lambda x: classify(x)))

    df['date'] = df['created_at'].apply(lambda x: x.date())

    total = len(df)
    total_pos = df['label'].value_counts()[1]
    total_neg = df['label'].value_counts()[0]
    total_neu = 0

    idx_max_pos = df[df['label'] == 'POSITIVE']['score'].idxmax()
    idx_max_neg = df[df['label'] == 'NEGATIVE']['score'].idxmax()
    idx_max_retweets = df['retweet_count'].idxmax()

    id_max_pos = df.iloc[idx_max_pos]['id']
    id_max_neg = df.iloc[idx_max_neg]['id']
    id_max_retweets = df.iloc[idx_max_retweets]['id']

    dates = df.groupby('date').count().reset_index()['date']
    dates = list(dates.apply(lambda x: x.strftime("%d/%m/%Y")))
    tweets_per_day = list(df.groupby('date').count().reset_index()['id'])

    line_df = df.groupby(['date', 'label']).count().reset_index()

    line_df = line_df.pivot(index='date', columns='label', values='id').reset_index()

    def f(row):
        if np.isnan(row['NEGATIVE']) and ~np.isnan(row['POSITIVE']):
            val = 100
        elif ~np.isnan(row['NEGATIVE']) and np.isnan(row['POSITIVE']):
            val = 0
        else:
            val = 100 * (row['POSITIVE'] / (row['POSITIVE'] + (row['NEGATIVE'])))
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
            'id_max_retweets': id_max_retweets
            }
        }

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

    json_data = json.dumps(dict_data, cls=NpEncoder)

    return json_data

if __name__ == '__main__':
    pass