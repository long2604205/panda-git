from git import Repo, InvalidGitRepositoryError, GitCommandError, FetchInfo
import os

class GitService:
    @staticmethod
    def clone_repo(repo_url, destination=None):
        if not destination:
            destination = os.path.basename(repo_url).replace(".git", "")
        Repo.clone_from(repo_url, destination)

    @staticmethod
    def open_repo(repo_path):
        try:
            repo = Repo(repo_path)

            # Lấy tên repo (tên folder)
            name = os.path.basename(repo_path)

            # Trạng thái sạch hay không
            status = "clean" if not repo.is_dirty(untracked_files=True) else "dirty"

            # Nhánh hiện tại
            current_branch = repo.active_branch.name if not repo.head.is_detached else "DETACHED"

            # Danh sách nhánh
            local_branches = [head.name for head in repo.heads]
            remote_branches = []
            for remote in repo.remotes:
                for ref in remote.refs:
                    remote_branches.append(str(ref.name))

            # File đã thay đổi
            changed_files = []
            diff_index = repo.index.diff(None)  # So với working tree
            untracked = repo.untracked_files

            file_id = 1
            for diff in diff_index:
                file_path = diff.a_path
                changed_files.append({
                    "id": file_id,
                    "name": os.path.basename(file_path),
                    "path": os.path.dirname(file_path).replace('/', '\\'),
                    "type": os.path.splitext(file_path)[1][1:]
                })
                file_id += 1

            for file_path in untracked:
                changed_files.append({
                    "id": file_id,
                    "name": os.path.basename(file_path),
                    "path": os.path.dirname(file_path).replace('/', '\\'),
                    "type": os.path.splitext(file_path)[1][1:]
                })
                file_id += 1

            return {
                "id": name,
                "name": name,
                "path": os.path.abspath(repo_path),
                "status": status,
                "currentBranch": current_branch,
                "branches": {
                    "local": local_branches,
                    "remote": remote_branches
                },
                "changes": changed_files
            }

        except InvalidGitRepositoryError:
            raise Exception(f"Invalid Git repo: {repo_path}")
        except GitCommandError as e:
            raise Exception(f"Git error: {str(e)}")

    @staticmethod
    def checkout_branch(repo_path: str, branch_name: str):
        try:
            repo = Repo(repo_path)

            # Nếu nhánh đã tồn tại local -> checkout luôn
            if branch_name in repo.heads:
                repo.git.checkout(branch_name)
                return {
                    "message": f"Checked out to local branch '{branch_name}'",
                    "currentBranch": branch_name
                }

            # Nếu không tồn tại local, kiểm tra remote
            full_remote_branch = f"origin/{branch_name}"
            remote_branches = [str(ref.name) for remote in repo.remotes for ref in remote.refs]
            if full_remote_branch in remote_branches:
                # Tạo local tracking branch từ remote
                repo.git.checkout('-b', branch_name, full_remote_branch)
                return {
                    "message": f"Created and checked out to new local branch from remote '{full_remote_branch}'",
                    "currentBranch": branch_name
                }

            raise Exception(f"Branch '{branch_name}' not found in local or remote")

        except (InvalidGitRepositoryError, GitCommandError) as e:
            raise Exception(f"Checkout error: {str(e)}")

    @staticmethod
    def commit_changes(repo_path: str, message: str, files: list[str], amend=False, signoff=False, push=False):
        try:
            repo = Repo(repo_path)

            if not message.strip():
                raise Exception("Commit message cannot be empty.")

            # Nếu không có file nào được chọn
            if not files:
                raise Exception("No files specified to commit.")

            # Add từng file cụ thể
            for file in files:
                abs_path = os.path.join(repo_path, file)
                if os.path.exists(abs_path):
                    repo.git.add(file)
                else:
                    raise Exception(f"File not found: {file}")

            # Kiểm tra có gì để commit không
            if not repo.index.diff("HEAD"):
                raise Exception("Nothing to commit.")

            # Build commit options
            commit_options = []
            if amend:
                commit_options.append("--amend")
            if signoff:
                commit_options.append("--signoff")

            # Commit
            repo.git.commit("-m", message, *commit_options)

            latest_commit = repo.head.commit

            # Nếu cần push
            if push:
                repo.git.push()

            return {
                "message": "Commit successful.",
                "commit_hash": latest_commit.hexsha,
                "commit_message": latest_commit.message.strip(),
                "author": latest_commit.author.name,
                "date": latest_commit.committed_datetime.isoformat()
            }

        except (InvalidGitRepositoryError, GitCommandError) as e:
            raise Exception(f"Commit error: {str(e)}")
    @staticmethod
    def push_changes(repo_path: str):
        try:
            repo = Repo(repo_path)

            # Lấy nhánh hiện tại
            current_branch = repo.active_branch.name

            # Push lên origin
            origin = repo.remote(name='origin')

            push_result = origin.push(refspec=current_branch)
            push_info = push_result[0]

            if push_info.flags & push_info.ERROR:
                raise Exception(f"Push failed: {push_info.summary}")

            return {
                "message": f"Pushed branch '{current_branch}' to origin successfully.",
                "branch": current_branch,
                "summary": push_info.summary
            }

        except Exception as e:
            raise Exception(f"Push error: {str(e)}")

    @staticmethod
    def pull_changes(repo_path: str):
        try:
            repo = Repo(repo_path)

            current_branch = repo.active_branch.name
            origin = repo.remote(name='origin')

            # Pull từ remote
            pull_infos = origin.pull(current_branch)

            if not pull_infos:
                raise Exception("Nothing was pulled.")

            pull_info = pull_infos[0]

            # Check lỗi (dựa vào flags)
            if pull_info.flags & FetchInfo.ERROR:
                raise Exception("Pull failed.")

            return {
                "message": f"Pulled branch '{current_branch}' from origin successfully.",
                "branch": current_branch,
                "remote_ref": pull_info.ref.name,
                "local_commit": pull_info.commit.hexsha,
                "note": pull_info.note or "Updated successfully"
            }

        except Exception as e:
            raise Exception(f"Pull error: {str(e)}")

    @staticmethod
    def fetch_remote(repo_path: str):
        try:
            repo = Repo(repo_path)
            origin = repo.remote(name='origin')

            fetch_infos = origin.fetch()  # fetch all refs

            results = []
            for info in fetch_infos:
                result = {
                    "ref": info.ref.name,
                    "remote_commit": info.commit.hexsha,
                    "note": info.note or "Fetched"
                }
                results.append(result)

            return {
                "message": f"Fetched from origin successfully.",
                "fetched_refs": results
            }

        except (InvalidGitRepositoryError, GitCommandError) as e:
            raise Exception(f"Fetch error: {str(e)}")

    @staticmethod
    def merge_branch(repo_path: str, source_branch: str):
        try:
            repo = Repo(repo_path)

            if repo.is_dirty(untracked_files=True):
                raise Exception("Repository has uncommitted changes. Please commit or stash before merging.")

            # Lấy nhánh hiện tại
            current_branch = repo.active_branch.name

            if current_branch == source_branch:
                raise Exception("Cannot merge a branch into itself.")

            # Đảm bảo source_branch tồn tại
            if source_branch not in repo.heads:
                raise Exception(f"Source branch '{source_branch}' does not exist locally.")

            # Merge
            merge_result = repo.git.merge(source_branch)

            return {
                "message": f"Merged branch '{source_branch}' into '{current_branch}' successfully.",
                "current_branch": current_branch,
                "merged_from": source_branch,
                "result": merge_result
            }

        except GitCommandError as e:
            if 'merge conflict' in str(e).lower():
                return {
                    "message": f"Merge conflict occurred while merging '{source_branch}' into '{current_branch}'",
                    "current_branch": current_branch,
                    "merged_from": source_branch,
                    "conflict": True,
                    "details": str(e)
                }
            raise Exception(f"Merge error: {str(e)}")

        except Exception as e:
            raise Exception(f"Merge error: {str(e)}")