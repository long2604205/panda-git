from app.domains.git.repository.repository_route import register_repository_routes


def register_git_routes(app):
    register_repository_routes(app)
