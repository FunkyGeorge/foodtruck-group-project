from system.core.model import Model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def getUser(self, id):
        query = "SELECT * FROM users where id = :id"
        data = {'id': id}
        return self.db.query_db(query, data)

    def validateEmail(self, form):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        valid = True
        errors = []
        if not form['email']:
            errors.append("Email cannot be blank")
            valid = False
        elif not EMAIL_REGEX.match(form['email']):
            errors.append("Invalid Email")
            valid = False

        return {"valid": valid, "errors": errors}

    def validateInfo(self, form):
        valid = True
        errors = []

        if not form['fname']:
            errors.append("First Name cannot be empty")
            valid = False

        if not form['lname']:
            errors.append("Last Name cannot be empty")
            valid = False

        return {"valid": valid, "errors": errors}

	def validateNumber(self, form):
		valid = True
		errors = []

		if not form['number']:
			errors.append("Please input your number")
			valid = False
		elif len(form['number']) < 10:
			errors.append("Number missing digits")
			valid = False
		return {'valid': valid, "errors": errors}

    def validatePassword(self, form):
        valid = True
        errors = []

        if not form['pword']:
            errors.append("Password cannot be empty")
            valid = False
        elif len(form['pword']) < 8:
            errors.append("Password has to be longer than 8 characters")
            valid = False
        elif not form['cword']:
            errors.append("You did not confirm your password")
            valid = False
        elif form['pword'] != form['cword']:
            errors.append("Passwords do not match")
            valid = False

        return {"valid": valid, "errors": errors}

    def addUser(self, form):
        query = "INSERT INTO users (first_name, last_name, email, access_key, created_at, updated_at, location, phone) "\
        "VALUES (:fname, :lname, :email, :key, NOW(), NOW(), :location, :number);"
        data = {
            'fname': form['fname'],
            'lname': form['lname'],
            'email': form['email'],
            'key': form['pword'], #Password not encrypted yet since not sure if use password or OAuth key
			'number': form['number'],
            'location': "(37.7749, -122.4194)"
        }
        return self.db.query_db(query, data)


    def validateLogin(self, data):
        query = "SELECT * FROM users WHERE email = :email AND access_key = :password"
        return self.db.query_db(query, data)
