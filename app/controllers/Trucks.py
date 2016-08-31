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

    
    def populateReviews(self):
        reviews = self.models['Truck'].getReviews(request.form)

        return jsonify(reviews)