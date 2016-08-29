from system.core.controller import *
import oauth2 as oauth
import json
import os
import signing


class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        CONSUMER_KEY = signing.consumer_key()
        CONSUMER_SECRET = signing.consumer_secret()
        ACCESS_KEY = signing.access_key()
        ACCESS_SECRET = signing.access_secret()

        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        global client
        client = oauth.Client(consumer, access_token)
        
        self.load_model('User')
        self.db = self._app.db
        self.twitter = oauth.remote_app('twitter',
            base_url='https://api.twitter.com/1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key='<your key here>',
            consumer_secret='<your secret here>'
        )

        self.facebook = oauth.remote_app('facebook',
            base_url='https://graph.facebook.com/',
            request_token_url=None,
            access_token_url='/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            consumer_key=FACEBOOK_APP_ID,
            consumer_secret=FACEBOOK_APP_SECRET,
            request_token_params={'scope': 'email'}
        )

    # INDEX
    def index(self):
        print self.twitter, "self.twitter"
        return self.load_view('index.html')

