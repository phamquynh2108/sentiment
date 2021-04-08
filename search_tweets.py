import tweepy
from sentiment.twitter import MyStreamListener
import pandas as pd
from dotenv import dotenv_values

def sendData():
    config = dotenv_values(".env")
    key_word = pd.read_excel('keyword.xlsx')
    key_word = key_word['keyword'].to_list()[:15]

    twitter = MyStreamListener(key=config['CONSUMER_KEY'], secret=config['CONSUMER_KEY_SECRET'],
                               token=config['ACCESS_TOKEN'], token_secrect=config['ACCESS_TOKEN_SECRET'])
    # connect to Twitter API
    api = twitter.connect_api()
    myStream = tweepy.Stream(auth=api.auth, listener=twitter)

    myStream.filter(track=key_word, languages=['en'], encoding='utf8')

if __name__ == '__main__':
    sendData()
