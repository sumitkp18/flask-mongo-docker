from database.db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class User(db.Document):
    email = db.EmailField(unique = True, required = True)
    password = db.StringField(required=True, min_length=8)
    first_name = db.StringField(required=True,max_length=50)
    last_name = db.StringField(required=True, max_length=50)

    def hash_password(self):
        self.password  = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password,password)
