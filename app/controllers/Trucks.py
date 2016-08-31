from system.core.controller import *
from twilio.rest import TwilioRestClient
import twilioauth
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

def send_text(body):
    client = TwilioRestClient(twilioauth.account, twilioauth.token)
    client.messages.create(
        to='+12096200032',
        from_='+12097796165',
        body=body
    )

class Trucks(Controller):
    def __init__(self, action):
        super(Trucks, self).__init__(action)

        self.load_model('Truck')
        self.db = self._app.db


    # INDEX
    def index(self):
        send_text("testing123")
        self.createReminder()
        return self.load_view('index.html')

    def feedback(self):
        if not 'id' in session:
            # flash("Log in to use this feature")
            return jsonify({'status': 'true'})

        if not request.form['truckName']:
            return jsonify({'status': 'true'})
        if request.form['action'] == 'Favorite':
            truck = self.models['Truck'].getTruck(request.form['truckName'])
            self.models['Truck'].favorite(truck, session['id'])
        elif request.form['action'] == 'Leave a Review':
            truck = self.models['Truck'].getTruck(request.form['truckName'])
            #show review method

        return jsonify({'status': 'true'})

    def review(self):
        truck = self.models['Truck'].getTruck(request.form['action'])
        self.models['Truck'].leaveReview(truck, request.form, session['id'])
        return jsonify({'status': 'true'})

    
    def createReminder(self):
        scheduler.add_job(self.reminderText("testing456"), 60)

    def reminderText(self, body):
        send_text(body)
