from system.core.controller import *
import oauth2 as oauth
import json
import os


class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        # CONSUMER_KEY = signing.consumer_key()             #OAuth stuff
        # CONSUMER_SECRET = signing.consumer_secret()
        # ACCESS_KEY = signing.access_key()
        # ACCESS_SECRET = signing.access_secret()

        # consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        # access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
        # global client
        # client = oauth.Client(consumer, access_token)
        
        self.load_model('User')
        self.db = self._app.db
        # self.twitter = oauth.remote_app('twitter',
        #     base_url='https://api.twitter.com/1/',
        #     request_token_url='https://api.twitter.com/oauth/request_token',
        #     access_token_url='https://api.twitter.com/oauth/access_token',
        #     authorize_url='https://api.twitter.com/oauth/authenticate',
        #     consumer_key='<your key here>',
        #     consumer_secret='<your secret here>'
        # )

        # self.facebook = oauth.remote_app('facebook',
        #     base_url='https://graph.facebook.com/',
        #     request_token_url=None,
        #     access_token_url='/oauth/access_token',
        #     authorize_url='https://www.facebook.com/dialog/oauth',
        #     consumer_key=FACEBOOK_APP_ID,
        #     consumer_secret=FACEBOOK_APP_SECRET,
        #     request_token_params={'scope': 'email'}
        # )

    # INDEX
    def index(self):
        return self.load_view('index.html')

    def logout(self):
        session.clear()
        return redirect('/')

    def register(self):
        return self.load_view('authentication.html')

    def create(self):
        valid = True
        form = request.form
        check = self.models['User'].validateEmail(form)
        if not check['valid']:
            for error in check['errors']:
                print error
                flash(error, 'email')
                valid = False
        check = self.models['User'].validateInfo(form)
        if not check['valid']:
            for error in check['errors']:
                flash(error, 'info')
                valid = False
        check = self.models['User'].validatePassword(form)
        if not check['valid']:
            for error in check['errors']:
                print error
                flash(error, 'password')
                valid = False
        
        if valid:
            session['id'] = self.models['User'].addUser(form)
            return redirect('/')
        else:
            return self.load_view('authentication.html')

    def login(self):
        user = self.models['User'].validateLogin(request.form)
        if user:
            session['id'] = user[0]['id']
            print "ok"
        else:
            flash("Incorrect Username/Password")
            print "error"
        return redirect('/')





















