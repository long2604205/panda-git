from app.services.git_service import GitService
from app.utils.response import JsonResponse

class GitController:
    @staticmethod
    def clone_repo(request):
        data = request.get_json()
        if not data or "repo_url" not in data:
            return JsonResponse.error("Missing required field: 'repo_url'", status_code=400)

        repo_url = data["repo_url"]
        destination = data.get("destination")

        try:
            GitService.clone_repo(repo_url, destination)
            result = GitService.open_repo(destination)
            return JsonResponse.success(result, message="Repository cloned successfully")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def open_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data:
            return JsonResponse.error("Missing required field: 'repo_path'", status_code=400)

        repo_path = data["repo_path"]
        try:
            repo = GitService.open_repo(repo_path)
            return JsonResponse.success(repo, message="Open repository successfully")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def checkout_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data or "branch_name" not in data:
            return JsonResponse.error("Missing required fields: 'repo_path' and 'branch_name'", status_code=400)

        repo_path = data["repo_path"]
        branch_name = data["branch_name"]

        try:
            result = GitService.checkout_branch(repo_path, branch_name)
            return JsonResponse.success(result, message=f"Checked out to branch '{branch_name}' successfully")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def commit_repo(request):
        data = request.get_json()
        if not data:
            return JsonResponse.error("Missing request data", status_code=400)

        repo_path = data.get("repo_path")
        message = data.get("message")
        files = data.get("files", [])
        amend = data.get("amend", False)
        signoff = data.get("signoff", False)
        push = data.get("push", False)

        if not repo_path or not message or not files:
            return JsonResponse.error("Missing required fields: 'repo_path', 'message', or 'files'", status_code=400)

        try:
            result = GitService.commit_changes(repo_path, message, files, amend, signoff, push)
            return JsonResponse.success(result, message="Commit created successfully")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def push_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data:
            return JsonResponse.error("Missing required field: 'repo_path'", status_code=400)

        repo_path = data["repo_path"]

        try:
            result = GitService.push_changes(repo_path)
            return JsonResponse.success(result, message="Push successful")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def pull_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data:
            return JsonResponse.error("Missing required field: 'repo_path'", status_code=400)

        repo_path = data["repo_path"]

        try:
            result = GitService.pull_changes(repo_path)
            return JsonResponse.success(result, message="All files are up to date")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def fetch_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data:
            return JsonResponse.error("Missing required field: 'repo_path'", status_code=400)

        repo_path = data["repo_path"]

        try:
            result = GitService.fetch_remote(repo_path)
            return JsonResponse.success(result, message="Fetch successful")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def merge_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data or "source_branch" not in data:
            return JsonResponse.error("Missing required fields: 'repo_path' and 'source_branch'", status_code=400)

        repo_path = data["repo_path"]
        source_branch = data["source_branch"]

        try:
            result = GitService.merge_branch(repo_path, source_branch)

            if result.get("conflict"):
                return JsonResponse.success(result, message="Merge conflict detected")

            return JsonResponse.success(result, message="Merge successful")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)

    @staticmethod
    def rename_repo(request):
        data = request.get_json()
        if not data or "repo_path" not in data or "new_name" not in data:
            return JsonResponse.error("Missing required fields: 'repo_path' and 'new_name'", status_code=400)

        repo_path = data["repo_path"]
        new_name = data["new_name"]

        try:
            data = GitService.rename_repo(repo_path, new_name)
            return JsonResponse.success({
                "name": data["name"],
                "path": data["path"],
            },
                message="Repository renamed successfully")
        except Exception as e:
            return JsonResponse.error(str(e), status_code=500)