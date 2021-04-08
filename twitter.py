from loguru import logger
import sys
import tweepy
from sentiment.database import MongoDatabase


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, key, secret, token, token_secrect):
        logger.info('Initialize {}'.format(self.__class__.__name__))
        self.key = key
        self.secret = secret
        self.token = token
        self.token_secrect = token_secrect

        self.auth = tweepy.OAuthHandler(self.key, self.secret)
        self.auth.set_access_token(token, token_secrect)

    def connect_api(self):
        logger.info('Called function: {}.{} '.format(self.__class__.__name__, sys._getframe().f_code.co_name))
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return self.api

    def on_status(self, status):
        try:
            #check if text has been truncated
            if hasattr(status,"extended_tweet"):
                text = status.extended_tweet["full_text"]
            else:
                text = status.text

            # if "retweeted_status" attribute exists, flag this tweet as a retweet
            # if hasattr(status,"retweeted_status"):  #returns True if the specified object has the specified attribute
            is_retweet = hasattr(status, "retweeted_status")
            retweeted_text = ""
            if is_retweet:
                # check if quoted tweet's text has been truncated before recording it
                if hasattr(status, "extended_tweet"):  # Check if Retweet
                    retweeted_text = status.retweeted_status.extended_tweet["full_text"]
                else:
                    retweeted_text = status.retweeted_status.text

            #check if quoted tweet's text has been truncated before recording it
            is_quote = hasattr(status, "quoted_status")
            quoted_text = ""
            if is_quote:
                # check if quoted tweet's text has been truncated before recording it
                if hasattr(status.quoted_status, "extended_tweet"):
                    quoted_text = status.quoted_status.extended_tweet["full_text"]
                else:
                    quoted_text = status.quoted_status.text

            dict_ = {}
            dict_['date'] = status.created_at
            dict_['text'] = text
            dict_['is_retweet'] = is_retweet
            dict_['retweeted_text'] = retweeted_text
            dict_['is_quote'] = is_quote
            dict_['quoted_text'] = quoted_text
            dict_['favourites_count'] = status.user.favourites_count
        #    dict_['reply_count'] = status.reply_count

            db = MongoDatabase(client='twitterdb')
            #save document to database
            print(dict_)
            db.insert_one_to_collection(collection='raw_tweets', doc=dict_)

        except Exception as e:
            logger.error('[{}] : {}'.format(sys._getframe().f_code.co_name, e))
            exit(1)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

