# fitumi_initialize.py

# import twitter API
from twitter_API import *

# define fixed rewards
def fixed_rewards():
    s3 = Score(100, 'Nice to meet you! Answering our questions earnes you another 100 points!', '')
    s2 = Score(50, 'Congratulations! You receive 50 points for connecting your Twitter account!', '')
    s1 = Score(50, 'Thank you for installing the app! You get 50 points!', '')
    ss = [s3, s2, s1]    
    return ss

# calculate total score
def total_score(user_scores):
    score = 0
    for user_score in user_scores:
        score = score + user_score.value
    return score        

# main object
class TwitterInitialize:

    def initialize(self, user_id, access_token, access_token_secret, consumer_key, consumer_secret):
        """Initializes the user object"""

        # start twitter API
        api = invoke_api(consumer_key, consumer_secret, access_token, access_token_secret)

        # get user properties
        user = api.me()
        last_tweet_id = user.status._json['id']

        # get first scores
        user_scores = fixed_rewards()
        current_score = total_score(user_scores)
        
        # return user properties
        return User(user_id, last_tweet_id, current_score, user_scores)

# user object
class User:
    def __init__(self, twitterUserID : int, lastPostedTweetId : int, totalRating : int, allTweetsRating : list):
        self.twitterUserID = twitterUserID
        self.lastPostedTweetId= lastPostedTweetId
        self.totalRating = totalRating
        self.allTweetsRating = allTweetsRating

# score object
class Score:
    def __init__(self, value : int, notification : str, tweet : str):
        self.value = value
        self.notification = notification
        self.tweet = tweet
