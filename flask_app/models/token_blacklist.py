from database.db import db


class TokenBlacklist(db.Document):
    token = db.StringField(required=True)