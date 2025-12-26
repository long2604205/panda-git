from app.utils.json_response import JsonResponse

from app.domains.git.repository.repository_service import RepositoryService


class RepositoryController:
    def __init__(self):
        pass

    @staticmethod
    def open_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data:
            return JsonResponse.error("Missing required field: 'repo_path'", status_code=400)

        repo_path = data["repo_path"]
        try:
            repo = RepositoryService.open_repo(repo_path)
            return JsonResponse.success(repo, message="Open repository successfully")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)