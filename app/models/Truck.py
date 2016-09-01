from system.core.model import Model


class Truck(Model):
    def __init__(self):
        super(Truck, self).__init__()

    def getTruck(self, name):
        query = "SELECT * FROM trucks WHERE name = :name"
        data = {'name': name}
        truck = self.db.query_db(query, data)
        if truck:
        	return truck[0]['id']
        else:
        	query = "INSERT INTO trucks (name) VALUES (:name)"
        	truck = self.db.query_db(query, data)
            
        	return truck


    def favorite(self, truck, user):
    	sql = "INSERT INTO favorites (user_id, truck_id) VALUES (:user,:truck)"
    	data ={
    		'user': user,
    		'truck': truck
    	}
    	self.db.query_db(sql, data)

    	return True

    def unFav(self, truck, user):
        sql = "DELETE FROM favorites WHERE user_id = :user AND truck_id = :truck"
        data ={
            'user': user,
            'truck': truck
        }
        self.db.query_db(sql, data)
        return True

    def leaveReview(self, truck, form, id):
        sql = "INSERT INTO reviews (review, rating, created_at, updated_at, user_id, truck_id) "\
        "VALUES (:review, :rating, NOW(), NOW(), :id, :truck)"
        data = {
            'review': form['text'],
            'rating': form['rate'],
            'id': id,
            'truck': truck
        }
        self.db.query_db(sql, data)
        return True

    def getReviews(self, form):
        query = '''SELECT r.review, r.rating, DATE_FORMAT(r.updated_at, '%b-%e-%Y %I:%i%p') as updated_at, u.first_name FROM reviews r
            JOIN users u on u.id = r.user_id
            WHERE truck_id IN 
            (SELECT id FROM trucks WHERE name = :name)'''
        data = {
            'name': form['action']
        }
        return self.db.query_db(query,data) 

    def getRating(self, form):
        query = '''SELECT ifnull(avg(rating), 0) as avg from reviews WHERE truck_id IN 
        (SELECT id FROM trucks WHERE name = :name)'''
        data = {
            'name': form['action']
        }
        stars = self.db.query_db(query, data)
        stars = stars[0]['avg']
        
        return stars


    def favsList(self, id):
        query = '''SELECT name FROM favorites f
            JOIN trucks t ON f.truck_id = t.id
            WHERE user_id = :id'''
        data = {'id': id}
        return self.db.query_db(query, data)












