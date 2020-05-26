from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models.user import User

from models.errors import InternalServerError


class Default(Resource):
    """
    Get request to "/"
    """

    def get(self):
        response = "Congratulations! The Flask App is up and running"
        return response, 200


class DashboardApi(Resource):
    """
    API resouce for revoking access token.
    """

    @jwt_required
    def get(self):
        try:
            current_user_id = get_jwt_identity()
            user = User.objects.get(id=current_user_id)
            name = user.first_name + " " + user.last_name
            response = "Hello {}, Welcome to your Dashboard!".format(name)
            return response, 200
        except Exception:
            raise InternalServerError
