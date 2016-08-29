from system.core.model import Model
emailRegex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()

    def create(self, data): # VALIDATIONS LOCATED BELOW. https://github.com/ZakStrassberg/user-dashboard-pylot/blob/master/app/models/User.py#L81
        query = "INSERT into table (column) values(:key)"
        data = {'key': 'value'}
        self.db.query_db(query, data)
        return True

    def get_all(self):
        query = "SELECT * FROM _"
        return self.db.query_db(query)

    def get(self, id):
        query = "SELECT * from users where id = :id"
        data = {'id': id}
        return self.db.get_one(query, data)

    def update(self, id):
        query = "UPDATE table SET colum=:key"
        data = {'key': value}
        self.db.query_db(query, data)
        return True

    def destroy(self, id):
        query = "DELETE FROM table WHERE id=:id"
        data = {'id': id}
        self.db.query_db(query, data)
        return True

    ### VALIDATION ###
    # Name: {'value': name to validate, 'flash': prefix for flash msg}
    # errors: list of errors
    # def validate_name(self, name, errors):
    #     if len(name['value'].strip()) < 2:
    #         errors.append({'error': "{} too short".format(name['flash'])})
    #     elif not name['value'].isalpha():
    #         errors.append({'error': "{} must be letters only".format(
    #             name['flash'])})
    #
    # def validate_email(self, email, errors, checkdupeemail=True):
    #     if not emailRegex.match(email):
    #         errors.append({'error': "Invalid email address!"})
    #     elif checkdupeemail:
    #         # CHECK WHETHER EMAIL IS ALREADY IN DB
    #         query = 'SELECT * FROM users WHERE email=:email'
    #         email = {'email': email}
    #         if self.db.query_db(query, email):
    #             errors.append({'error': "email already in database"})
    #
    # def validate_password(self, password, passwordconf, errors):
    #     if len(password) < 8:
    #         errors.append({'error': "Password must be at least 8 characters"})
    #     elif password != passwordconf:
    #         errors.append({'error': "Passwords do not match"})
    # def login_user(self, info):
    #     query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    #     data = {'email': info['email']}
    #     user = self.db.get_one(query, data)
    #     if user:
    #         if self.bcrypt.check_password_hash(user.password, info['password']):
    #             return user
    #     return False
