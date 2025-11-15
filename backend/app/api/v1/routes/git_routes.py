from flask import request
from app.controllers.git_controller import GitController

def register_git_routes(app):
    @app.route("/clone", methods=["POST"])
    def clone_repo():
        return GitController.clone_repo(request)

    @app.route("/open-repository", methods=["POST"])
    def open_repo():
        return GitController.open_repo(request)

    @app.route("/checkout-branch", methods=["POST"])
    def checkout():
        return GitController.checkout_repo(request)

    @app.route("/commit", methods=["POST"])
    def commit():
        return GitController.commit_repo(request)

    @app.route("/push", methods=["POST"])
    def push():
        return GitController.push_repo(request)

    @app.route("/pull", methods=["POST"])
    def pull():
        return GitController.pull_repo(request)

    @app.route("/fetch", methods=["POST"])
    def fetch():
        return GitController.fetch_repo(request)

    @app.route("/merge", methods=["POST"])
    def merge():
        return GitController.merge_repo(request)

    @app.route("/rename", methods=["POST"])
    def rename():
        return GitController.rename_repo(request)
