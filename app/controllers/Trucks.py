from system.core.controller import *
from twilio.rest import TwilioRestClient
import twilioauth
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
sched.start()

class Trucks(Controller):
    def __init__(self, action):
        super(Trucks, self).__init__(action)

        self.load_model('Truck')
        self.load_model('User')
        self.db = self._app.db


    # INDEX
    def index(self):
        return self.load_view('index.html')

    def favorite(self):
        if not 'id' in session:
            return jsonify({'status': 'false'})

        truck = self.models['Truck'].getTruck(request.form['truckName'])
        if request.form['favorite'] == '1':
            self.models['Truck'].favorite(truck, session['id'])
        elif request.form['favorite'] == '0':
            self.models['Truck'].unFav(truck, session['id'])
            return jsonify({'status': 'true'})


    def review(self):
        truck = self.models['Truck'].getTruck(request.form['action'])
        self.models['Truck'].leaveReview(truck, request.form, session['id'])
        return jsonify({'status': 'true'})

    def populateReviews(self):
        reviews = self.models['Truck'].getReviews(request.form)
        return self.load_view('_getReviews.html', reviews=reviews)

    def getRating(self):
        rating = self.models['Truck'].getRating(request.form)
        rating='{0:.2g}'.format(rating)
        return jsonify({'rating': rating})

    def getFavs(self):
        if 'id' in session:
            favorites = self.models['Truck'].favsList(session['id']);
            return jsonify({'favorites': favorites});
        else:
            return jsonify({'status': 'false'});


#---------------Twilio Stuff------------------------------------------
    def configReminder(self):
        user = self.models['User'].getUser(session['id'])
        data = {
            'user': user[0]['first_name'],
            'phone': '+19092578727',
            'truck': request.form['truckName'],
            'time': request.form['date']
        }
        body = "Hello " + data['user'] + " you have set a reminder for " + data['truck'] + " at " + data['time']
        send_text(body, data['phone'])
        self.createReminder(data)
        return jsonify({'status': 'true'})

    def createReminder(self, data):
        #get formatted date
        #get arg string
        body = data['truck'],"is here!!"
        sched.add_job(self.reminderText, 'date', run_date=data['time'], args=[body, data['phone']])

    def reminderText(self, body, number):
        send_text(body, number)

def send_text(body, number):
    client = TwilioRestClient(twilioauth.account, twilioauth.token)
    #Format number?
    client.messages.create(
        to=number,
        from_='+12016853820',
        body=body
    )



































