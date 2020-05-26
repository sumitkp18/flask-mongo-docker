import datetime

from flask import request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from flask_restful import Resource

from mongoengine.errors import NotUniqueError, DoesNotExist, ValidationError
from models.errors import SchemaValidationError, EmailAlreadyExistsError, InternalServerError, UnauthorizedError, \
    TimeExpiredError

from models.token_blacklist import TokenBlacklist
from models.user import User

import time

# token expiry time in hours
access_token_expiry = 1
refresh_token_expiry = 24


def register_jwt_callbacks(jwt_manager):
    @jwt_manager.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """
        callback method for checking access/ refresh
        """
        try:
            jti = decrypted_token['jti']
            token = TokenBlacklist.objects.get(token=jti)
            return True
        except DoesNotExist:
            return False

    @jwt_manager.revoked_token_loader
    def revoked_token_callback():
        response = {
            "message": "Token has been revoked. Try logging in again"
        }
        return response, 401


def _auto_generate_password(first_name, last_name):
    """
    A method to generate password based on first and last name and a random number based on time in nanos.
    """
    special_chars = "!@#$%^&*?+"
    time_in_nano = str(time.time())
    special_char = special_chars[int(time_in_nano[-4])]
    trailing_digits = time_in_nano[-3:]
    return "{}{}{}{}".format(first_name[:3], last_name[-3:], special_char, trailing_digits)


def _validate_field_exists(field):
    if field is None:
        raise ValidationError


def _create_user(record, is_admin=False):
    email = record.get("email")
    _validate_field_exists(email)
    first_name = record.get("first_name")
    _validate_field_exists(first_name)
    last_name = record.get("last_name")
    _validate_field_exists(last_name)

    password = _auto_generate_password(first_name, last_name)
    user = User(email=email, first_name=first_name, last_name=last_name, password=password)
    user.hash_password()
    user.save()
    return {'id': str(user.id), "email": email, "password": password}


class SignupApi(Resource):
    """
    API resource for sign-up
    """

    def post(self):
        try:
            body = request.get_json()
            response = _create_user(body)
            return response, 201
        except ValidationError:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class LoginApi(Resource):
    """
    API resource for log-in
    """

    def post(self):
        try:
            body = request.get_json()
            email = body.get('email')
            _validate_field_exists(email)
            password = body.get('password')
            _validate_field_exists(password)
            user = User.objects.get(email=email)
            authorized = user.check_password(password)
            if not authorized:
                raise UnauthorizedError
            access_token_expires = datetime.timedelta(hours=access_token_expiry)
            refresh_token_expires = datetime.timedelta(hours=refresh_token_expiry)
            access_token = create_access_token(identity=str(user.id), expires_delta=access_token_expires)
            refresh_token = create_refresh_token(identity=str(user.id), expires_delta=refresh_token_expires)
            response = {
                "access_token": access_token,
                "access_token_expiry": access_token_expiry,
                "refresh_token": refresh_token,
                "refresh_token_expiry": refresh_token_expiry,
                "timeUnit": "hour"
            }
            return response, 200
        except TimeExpiredError:
            raise TimeExpiredError
        except ValidationError:
            raise SchemaValidationError
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError


class RefreshApi(Resource):
    """
    API resource for Refresh.
    """

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        response = {
            'access_token': create_access_token(identity=current_user)
        }
        return response, 200


class LogoutAccessTokenApi(Resource):
    """
    API resouce for revoking access token.
    """

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        token = {'token': jti}
        token_blacklist = TokenBlacklist(**token)
        token_blacklist.save()
        response = {
            "msg": "Revoked Access token"
        }
        return response, 200


class LogoutRefreshTokenApi(Resource):
    """
    API resouce for revoking refresh token.
    """

    @jwt_refresh_token_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        token = {'token': jti}
        token_blacklist = TokenBlacklist(**token)
        token_blacklist.save()
        response = {
            "msg": "Revoked Refresh token. Successfully logged out"
        }
        return response, 200
