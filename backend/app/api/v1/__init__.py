from flask import Blueprint
from app.api.v1.routes.git_routes import register_git_routes

v1_blueprint = Blueprint('v1', __name__)

def init_routes():
    register_git_routes(v1_blueprint)

init_routes()
