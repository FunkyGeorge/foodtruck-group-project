from system.core.controller import *
import oauth2 as oauth
import json
import os


class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.db = self._app.db

    # INDEX
    def index(self):
        if 'id' in session:
            user = self.models['User'].getUser(session['id'])
        else:
            user = ["User"]
        return self.load_view('index.html', user=user[0])

    def logout(self):
        session.clear()
        return redirect('/')

    def register(self):
        return self.load_view('login.html')

    def create(self):
        valid = True
        form = request.form
        check = self.models['User'].validateEmail(form)
        if not check['valid']:
            for error in check['errors']:
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
                flash(error, 'password')
                valid = False

        if valid:
            session['id'] = self.models['User'].addUser(form)
            return redirect('/')
        else:
            return self.load_view('login.html')

    def login(self):
        user = self.models['User'].validateLogin(request.form)
        if user:
            session['id'] = user[0]['id']
        else:
            flash("Incorrect Username/Password")
        return redirect('/')


    def show(self):

        return self.load_view('truckinfo.html')





















