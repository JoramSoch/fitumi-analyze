# sample.py

# import modules
import falcon
import fitumi_initialize
import fitumi_update
import json

# main object
class TwitterResource:
    
    def on_get(self, req, resp):
        """Handles GET requests"""
        
        # Example call:
        # URI.create("https://falcongw2.cfapps.eu10.hana.ondemand.com/twitter?userId="
        #           + user.getTwitterUserID() + "&token=" + user.getTwitterAccessToken() + "&secret="
        #           + user.getTwitterSecret() + "&lastTweetId=" + user.getLastPostedTweetId()));
        
        # read out input parameters
        user_id = req.get_param('userId')
        last_tweet_id = int(req.get_param('lastTweetId'))

        # get access token and secret
        access_token = req.get_param('token')
        access_token_secret = req.get_param('secret')
        
        # get consumer key and secret
        consumer_key = 'MISSING'
        consumer_secret = 'MISSING'

        # initialize user
        if last_tweet_id == 0:
            twitter = fitumi_initialize.TwitterInitialize()
            user_profile = twitter.initialize(user_id, access_token, access_token_secret, consumer_key, consumer_secret)
        # update user
        else:
            twitter = fitumi_update.TwitterUpdate()
            user_profile = twitter.update(user_id, last_tweet_id, access_token, access_token_secret, consumer_key, consumer_secret)

        # output JSON
        json_user = json.dumps(user_profile, default = lambda o: o.__dict__, sort_keys = True, indent = 4)
        resp.content_type = falcon.MEDIA_JSON
        resp.body = json_user

# call falcon API
api = falcon.API()
api.add_route('/twitter', TwitterResource())
