from services.resource import Default
from services.resource import DashboardApi


def initialize_resource_routes(api):
    api.add_resource(Default, "/")
    api.add_resource(DashboardApi, "/dashboard")
