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
