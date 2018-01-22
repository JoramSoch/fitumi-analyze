# fitumi_update.py

# import twitter API
from twitter_API import *
from data_analysis import *

# get search strings
def get_keywords():
    filename = 'fitumi_keywords.txt'
    file_obj = open(filename, 'r')
    file_txt = file_obj.readlines()
    keywords = [line[:-1] for line in file_txt]
    return keywords

# define fixed rewards
def fixed_rewards():
    s3 = Score(100, 'Nice to meet you! Answering our questions earns you another 100 points!', '')
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
class TwitterUpdate:

    def update(self, user_id, last_tweet_id, access_token, access_token_secret, consumer_key, consumer_secret):
        """Initializes the user object"""

        # start twitter API
        api = invoke_api(consumer_key, consumer_secret, access_token, access_token_secret)

        # get search strings
        keywords = get_keywords()

        # get user properties
        num_followers = len(get_followers(api, user_id))

        # search new tweets
        user_tweets = get_new_tweets(api, user_id, last_tweet_id)
        user_tweet_info = extract_tweet_info(api, user_tweets)

        # score new content
        user_scores = [];
        for tweet in user_tweet_info:
            val = 0
            msg = ''
            if is_relevant_tweet(tweet[3], keywords):
                # original tweet
                if tweet[0] == 0:
                    val = rate_combined(num_followers, tweet[6], tweet[7], tweet[8])
                    msg = 'Congratulations! You receive ' + str(int(val)) + ' points for this original tweet!'
                # retweet w/o comment
                elif tweet[0] == 1:
                    val = rate_combined(num_followers, 0, 0, 0)
                    msg = 'Congratulations! You receive ' + str(int(val)) + ' points for this retweet!'
                # retweet with comment
                elif tweet[0] == 2:
                    val = rate_combined(num_followers, tweet[6], tweet[7], tweet[8])
                    msg = 'Congratulations! You receive ' + str(int(val)) + ' points for this retweet with comment!'
                user_scores.append(Score(val, msg, tweet[3]))

        # score first tweet
        if len(user_scores) > 0:
            val = 100
            msg = 'Congratulations! You receive ' + str(val) + ' points for your first #FCB-related tweet!'
            txt = user_scores[-1].tweet
            user_scores.append(Score(val, msg, txt))

        # add fixed rewards
        user_scores.extend(fixed_rewards())
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
