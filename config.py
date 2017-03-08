#tweetbot config

import tweepy
import time
from dailysep import *

CONSUMER_KEY = '_your_consumer_key_'
CONSUMER_SECRET = '_your_secret_'
ACCESS_KEY = '_your_access_key_'
ACCESS_SECRET = '_your_access_secret_'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#start by creating dicts       
dict_entry_url, dict_entry_date, dict_cp  = make_dicts()

#start flag to schedule tweets; will be updated later on by schedule_tweet
last_tweet_time = datetime.datetime.strptime("21/11/06 12:30", "%d/%m/%y %H:%M")
last_update = datetime.datetime.now()
p_counter = 0

while True:
    try:
        message, dict_cp, last_tweet_time = schedule_tweet(last_tweet_time, dict_cp, dict_entry_url, last_update)
        message = 'Entry # {0}: '.format(p_counter)+message
        api.update_status(message)
        p_counter+=1
    except:
        print 'sleep for 6 hours...'
        time.sleep(21600)
        pass


