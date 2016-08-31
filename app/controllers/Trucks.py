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
            return jsonify({'status': 'false'})

        if not request.form['truckName']:
            return jsonify({'status': 'false'})
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
       return self.load_view('_getReviews', reviews=reviews)

    def getRating(self):
        rating = self.models['Truck'].getRating(request.form)
        rating='{0:.2g}'.format(rating)
        return jsonify({'rating': rating})

    def getFavs(self):
        if 'id' in session:
            favorites = self.models['Truck'].favsList(session['id'])
            return jsonify(favorites)
        else:
            return jsonify({'status': 'false'})