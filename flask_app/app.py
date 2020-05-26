import os

from database.db import initialize_db
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from models.errors import errors
from routes.resource_routes import initialize_resource_routes
from routes.auth_routes import initialize_auth_routes
from services.auth import register_jwt_callbacks


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['PROPAGATE_EXCEPTIONS'] = True
db_host = os.environ['MONGODB_HOST']
db_name = os.environ['MONGODB_NAME']
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://' + db_host + ':27017/' + db_name
}

host = app.config['HOST']
port = app.config['PORT']

initialize_db(app)
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
initialize_auth_routes(api)
initialize_resource_routes(api)
jwt = JWTManager(app)
register_jwt_callbacks(jwt)

app.run(host=host, port=port, debug=False)
