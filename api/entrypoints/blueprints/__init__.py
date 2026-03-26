from flask import Blueprint

from api.entrypoints.blueprints.v1 import v1_routes

app_bp = Blueprint("app", __name__)

versioned_routes = [
    ("/v1", v1_routes),
    # ("/v2", v2_routes),
]

for prefix, routes in versioned_routes:
    for route in routes:
        app_bp.register_blueprint(route, url_prefix=prefix)
