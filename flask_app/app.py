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


def config(app):
    app.config.from_envvar('ENV_FILE_LOCATION')

    # JWT config
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # DB config
    db_host = os.environ['MONGODB_HOST']
    db_name = os.environ['MONGODB_NAME']
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb://' + db_host + ':27017/' + db_name
    }


def init(app):
    """
    function to initialise"
    1. DB [MongoDB]
    2. Restful-API [flask-restful]
    3. Bcrypt
    """
    # DB initialization
    initialize_db(app)

    # API initialization along with custom errors and routes
    api = Api(app, errors=errors)
    initialize_auth_routes(api)
    initialize_resource_routes(api)

    # Setting up Bcrypt for password encryption
    bcrypt = Bcrypt(app)

    # JWT initialisation
    jwt = JWTManager(app)
    register_jwt_callbacks(jwt)


if __name__ =="__main__" :
    app = Flask(__name__)
    config(app)
    init(app)
    host = app.config['HOST']
    port = app.config['PORT']
    app.run(host=host, port=port, debug=False)
