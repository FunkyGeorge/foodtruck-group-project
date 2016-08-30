from system.core.controller import *



class Trucks(Controller):
    def __init__(self, action):
        super(Trucks, self).__init__(action)
        
        self.load_model('Truck')
        self.db = self._app.db
        

    # INDEX
    def index(self):
        
        return self.load_view('index.html')

    def feedback(self):
        if not 'id' in session:
            # flash("Log in to use this feature")
            return jsonify({'status': 'true'})

        print request.form
        if not request.form['truckName']:
            return jsonify({'status': 'true'})
        print "passed checks"
        if request.form['action'] == 'Favorite':
            truck = self.models['Truck'].getTruck(request.form['truckName'])
            self.models['Truck'].favorite(truck, session['id'])
        elif request.form['action'] == 'Leave a Review':
            truck = self.models['Truck'].getTruck(request.form['truckName'])
            #add a review

        return jsonify({'status': 'true'})

    
