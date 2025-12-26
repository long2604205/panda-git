from flask import request

from app.domains.git.repository.repository_controller import RepositoryController


def register_repository_routes(app):
    @app.route("/clone", methods=["POST"])
    def clone_repo():
        return 'Cloning repository'

    @app.route("/open-repository", methods=["POST"])
    def open_repo():
        return RepositoryController.open_repo(request)
