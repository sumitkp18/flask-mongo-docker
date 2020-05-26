from services.auth import SignupApi
from services.auth import LoginApi
from services.auth import RefreshApi
from services.auth import LogoutAccessTokenApi
from services.auth import LogoutRefreshTokenApi


def initialize_auth_routes(api):
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(RefreshApi, '/api/auth/refresh')
    api.add_resource(LogoutAccessTokenApi, '/api/auth/logout_access')
    api.add_resource(LogoutRefreshTokenApi, '/api/auth/logout_refresh')
