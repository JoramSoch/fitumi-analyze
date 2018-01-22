import sys
import tweepy

import requests
from bs4 import BeautifulSoup

max_get_followers = 200
max_get_all_tweets = 200

def invoke_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def username2id(api, screen_name):
    user = api.get_user(screen_name)
    return user.id

def userid2name(api, user_id):
    user = api.get_user(user_id)
    return user.screen_name

def is_protected(api, user_id):
    user = api.get_user(user_id)
    return user.protected

def get_followings(api, user_id):
    following_ids = api.friends_ids(user_id)
    return following_ids

def get_followers(api, user_id):
    follower_ids = api.followers_ids(user_id, count=max_get_followers)
    return follower_ids

def get_all_tweets(api, user_id):
    # https://github.com/tweepy/tweepy/issues/853
    all_tweets = []
    new_tweets = api.user_timeline(user_id, count=100, tweet_mode='extended')
    all_tweets.extend(new_tweets)
    if new_tweets:
        oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0 & len(all_tweets) < max_get_all_tweets:
        new_tweets = api.user_timeline(user_id, count=100, max_id=oldest, tweet_mode='extended')
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
    return all_tweets

def get_new_tweets(api, user_id, last_tweet):
    new_tweets = api.user_timeline(user_id, since_id=last_tweet, tweet_mode='extended')
    return new_tweets

def number_of_replies(api, status_id):
    # https://stackoverflow.com/questions/46395855/is-there-any-way-to-get-the-number-of-comments-on-a-tweet-using-python
    status = api.get_status(status_id)
    status_url = 'https://twitter.com/' + status.user.screen_name + '/status/' + status.id_str
    html = requests.get(status_url)
    soup = BeautifulSoup(html.text, 'lxml')
    str_replies = soup.find_all('span', attrs={'class':'ProfileTweet-actionCountForAria'})[0].contents
    str_replies = str_replies[0][0:str_replies[0].find(' ')]
    num_replies = int(str_replies.replace('.',''))
    return num_replies

def extract_tweet_info(api, tweets):
    # initialize tweet info
    tweet_info = []
    for tweet in tweets:
    
        # get tweet basics
        tweet_id   = tweet.id
        tweet_time = tweet.created_at
        tweet_type = 0 # original tweet

        # get tweet text
        tweet_text = tweet._json['full_text']
        if hasattr(tweet, 'retweeted_status'):
            tweet_type = 1 # retweet w/o comment (= "retweet")
            tweet_text = 'RT @' + tweet._json['retweeted_status']['user']['screen_name'] + ': ' + tweet._json['retweeted_status']['full_text']
        if hasattr(tweet, 'quoted_status'):
            tweet_type = 2 # retweet with comment (= "quoted status")
            tweet_text = tweet_text + ' | RT @' + tweet._json['quoted_status']['user']['screen_name'] + ': ' + tweet._json['quoted_status']['full_text']
        
        # get hashtags
        hashtags = []
        for hashtag in tweet.entities['hashtags']:
            hashtags.append(hashtag['text'])
        
        # get usernames
        usernames = []
        for username in tweet.entities['user_mentions']:
            usernames.append(username['screen_name'])
        
        # get tweet likes
        num_likes    = tweet.favorite_count
        num_retweets = tweet.retweet_count
        num_replies  = number_of_replies(api, tweet_id)

        # store all information
        tweet_info.append((tweet_type, tweet_id, tweet_time, tweet_text, hashtags, usernames, num_likes, num_retweets, num_replies))

    # output tweet info
    return tweet_info
    
def get_translator():
    # https://stackoverflow.com/questions/32442608/ucs-2-codec-cant-encode-characters-in-position-1050-1050
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    return non_bmp_map
