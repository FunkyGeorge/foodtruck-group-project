from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        ## self.load_model('WelcomeModel')
        self.db = self._app.db

    # INDEX
    def index(self):
        return self.load_view('index.html')

    def new(self):
        return self.load_view('new.html')

    def create(self):
        # self.models[''].create()
        return redirect('/')

    def show(self, id):
        # param = self.models[''].get(id)
        return self.load_view('show.html', param=param)

    def edit(self, id):
        # param = self.models[''].get(id)
        return self.load_view('edit.html', param=param)

    def update(self, id):
        # self.models[''].update(id)
        return redirect('/')

    def destroy(self, id):
        # self.models[''].destroy(id)
        return redirect('/')
