from typing import Dict

import pygit2
from app.data.pre_pull_result import PrePullResult
from constants.constants import RepoStatus


class PullService:

    @staticmethod
    def _create_callbacks(username: str = None, password: str = None):
        """
        Helper tạo callback cho auth.
        Lưu ý: pygit2 yêu cầu trả về object RemoteCallbacks
        """
        if not username and not password:
            return None

        def creds_callback(url, username_from_url, allowed_types):
            # Ưu tiên SSH Key nếu có, hoặc UserPass nếu HTTP
            if allowed_types & pygit2.GIT_CREDTYPE_USERPASS_PLAINTEXT:
                return pygit2.UserPass(username, password)
            return None

        return pygit2.RemoteCallbacks(credentials=creds_callback)

    @staticmethod
    def _is_dirty(repo: pygit2.Repository) -> bool:
        """Kiểm tra trạng thái repo (Pure function)"""
        return bool(repo.status())

    @staticmethod
    def pull(
            repo_path: str,
            remote_name: str = 'origin',
            branch_name: str = 'main',
            auth_user: str = None,
            auth_pass: str = None
    ) -> Dict:
        """
        Static method thực hiện pull. Nhận input -> Trả output dict.
        Không lưu state trong class.
        """
        response = {
            "status": "UNKNOWN",
            "message": "",
            "details": {}
        }

        # 1. Init Repo ngay trong hàm (Stateless)
        try:
            repo = pygit2.Repository(repo_path)
        except pygit2.GitError:
            response["status"] = "ERROR"
            response["message"] = f"Invalid repository path: {repo_path}"
            return response

        try:
            # 2. Pre-flight Check: Dirty Worktree
            if PullService._is_dirty(repo):
                response["status"] = "DIRTY_WORKTREE"
                response["message"] = "Local changes detected. Commit or Stash before pulling."
                return response

            # 3. Fetch
            # Tìm remote
            try:
                remote = repo.remotes[remote_name]
            except KeyError:
                response["status"] = "ERROR"
                response["message"] = f"Remote '{remote_name}' not found."
                return response

            # Tạo callback auth từ tham số truyền vào
            callbacks = PullService._create_callbacks(auth_user, auth_pass)

            # Execute Fetch
            try:
                remote.fetch(callbacks=callbacks)
            except pygit2.GitError as e:
                response["status"] = "ERROR"
                response["message"] = f"Fetch failed: {str(e)}"
                return response

            # 4. Resolve References
            remote_ref_name = f'refs/remotes/{remote_name}/{branch_name}'
            try:
                remote_ref = repo.lookup_reference(remote_ref_name)
                remote_commit_id = remote_ref.target
            except KeyError:
                response["status"] = "ERROR"
                response["message"] = f"Remote branch '{branch_name}' does not exist."
                return response

            # 5. Merge Analysis
            analysis, _ = repo.merge_analysis(remote_commit_id)

            # --- Case: Up to date ---
            if analysis & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                response["status"] = "UP_TO_DATE"
                response["message"] = "Already up to date."
                return response

            # --- Case: Fast-forward ---
            elif analysis & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                # Checkout files
                repo.checkout_tree(repo.get(remote_commit_id))

                # Update Branch Ref
                branch_ref = repo.lookup_reference(f'refs/heads/{branch_name}')
                branch_ref.set_target(remote_commit_id)

                # Update HEAD
                repo.head.set_target(remote_commit_id)

                response["status"] = "SUCCESS"
                response["message"] = "Fast-forward successful."
                response["details"]["new_head"] = str(remote_commit_id)
                return response

            # --- Case: Normal Merge ---
            elif analysis & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                repo.merge(remote_commit_id)

                if repo.index.conflicts:
                    # --- CONFLICT ---
                    conflicts = list(set([c[0].path for c in repo.index.conflicts]))
                    response["status"] = "CONFLICT"
                    response["message"] = "Merge conflict detected."
                    response["details"]["conflicted_files"] = conflicts
                    return response
                else:
                    # --- MERGE COMMIT ---
                    user = repo.default_signature
                    tree = repo.index.write_tree()
                    parents = [repo.head.target, remote_commit_id]
                    message = f"Merge branch '{branch_name}' of {remote.url} into {branch_name}"

                    new_oid = repo.create_commit('HEAD', user, user, message, tree, parents)
                    repo.state_cleanup()

                    response["status"] = "SUCCESS"
                    response["message"] = "Merge commit created."
                    response["details"]["new_head"] = str(new_oid)
                    return response
            else:
                response["status"] = "ERROR"
                response["message"] = "Unknown merge state."
                return response

        except Exception as e:
            response["status"] = "ERROR"
            response["message"] = f"System error: {str(e)}"
            return response