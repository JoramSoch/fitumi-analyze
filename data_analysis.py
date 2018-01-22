from math import log10

max_rate_reach = 100000
weight_reach   = 0.5
weight_impact  = 0.5

def is_relevant_tweet(tweet_text, keywords): # , hashtags, usernames):
    kw_in_tweet = any(x in tweet_text for x in keywords)
    # ht_in_tweet = any(x in tweet_text for x in hashtags)
    # un_in_tweet = any(x in tweet_text for x in usernames)
    is_relevant = kw_in_tweet # | ht_in_tweet | un_in_tweet
    return is_relevant

def num_relevant_tweets(tweet_info, keywords):
    num_tweets = 0
    for tweet in tweet_info:
        if is_relevant_tweet(tweet[3], keywords):
            num_tweets = num_tweets + 1;
    return num_tweets

def rate_reach(num_followers):
    num_followers = num_followers + 1
    reach_score = round((log10(num_followers)/log10(max_rate_reach))*100,0)
    if reach_score > 100: reach_score = 100
    return reach_score

def rate_impact(num_followers, num_reactions):
    num_followers = num_followers + 1
    num_reactions = num_reactions + 1
    impact_score = round((log10(num_reactions)/log10(num_followers))*100,0)
    if impact_score > 100: impact_score = 100
    return impact_score

def rate_combined(num_followers, likes, retweets, comments):
    num_reactions  = likes + retweets + comments + 1
    combined_score = round(weight_reach  * rate_reach(num_followers) + weight_impact * rate_impact(num_followers, num_reactions),0)
    return combined_score
