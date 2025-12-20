import os
import re
import subprocess
from contextlib import suppress
import datetime
from git import Repo, NULL_TREE
import pygit2

from git import Repo, InvalidGitRepositoryError, GitCommandError, FetchInfo

class GitService:
    @staticmethod
    def clone_repo(repo_url, destination=None):
        if not destination:
            destination = os.path.basename(repo_url).replace(".git", "")
        Repo.clone_from(repo_url, destination)

    @staticmethod
    def open_repo2(repo_path):
        try:
            repo = Repo(repo_path)

            # Lấy tên repo (tên folder)
            name = os.path.basename(repo_path)

            # Trạng thái sạch hay không
            status = "clean" if not repo.is_dirty(untracked_files=True) else "dirty"

            # Nhánh hiện tại
            current_branch = repo.active_branch.name if not repo.head.is_detached else "DETACHED"

            # --------------------------
            # 1. Detect default branch
            # --------------------------
            default_branch = None
            try:
                ref = repo.git.symbolic_ref("refs/remotes/origin/HEAD")  # ví dụ: refs/remotes/origin/main
                default_branch = ref.split("/")[-1]  # main
            except:
                # fallback: nếu repo local mới init
                default_branch = "main" if "main" in [h.name for h in repo.heads] else "master"


            # Danh sách nhánh
            local_branches = [head.name for head in repo.heads]
            remote_branches = []
            for remote in repo.remotes:
                for ref in remote.refs:
                    remote_branches.append(str(ref.name).replace("refs/remotes/", ""))

            # --------------------------
            # 3. Sort function
            # --------------------------
            local_branches = GitService.sort_branches(local_branches, default_branch)
            remote_branches = GitService.sort_branches(remote_branches, default_branch)

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

    @staticmethod
    def rename_repo(old_path, new_name):
        if not os.path.isdir(old_path):
            raise Exception(f"Repo path does not exist: {old_path}")

        parent_dir = os.path.dirname(old_path)
        new_path = os.path.join(parent_dir, new_name)

        if os.path.exists(new_path):
            raise Exception(f"Target path already exists: {new_path}")

        print(f"[DEBUG] Renaming:\n old -> {old_path}\n new -> {new_path}")

        # Rename và bắt lỗi gốc
        try:
            os.rename(old_path, new_path)
        except Exception as e:
            raise Exception(f"Rename failed: {e}")

        # Kiểm tra rename thực sự thành công
        if os.path.exists(old_path):
            raise Exception("Rename failed: old_path still exists")

        if not os.path.isdir(new_path):
            raise Exception("Rename failed: new_path does not exist or is invalid")

        return {
            "name": new_name,
            "path": new_path
        }

    @staticmethod
    def sort_branches(branches, default_branch):
        def weight(name):
            # Nếu remote branch, lấy phần sau 'origin/' để sort
            short_name = name.split("/", 1)[-1] if name.startswith("origin/") else name

            if short_name == default_branch:
                return 0, short_name
            elif "/" not in short_name:
                return 1, short_name
            else:
                return 2, short_name

        return sorted(branches, key=weight)

    @staticmethod
    def get_initials(name):
        """Helper để tạo ký tự viết tắt (VD: Lion Wilson -> LW)"""
        if not name:
            return "??"
        parts = name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return parts[0][:2].upper()

    @staticmethod
    def get_graph_data(repo_path, branch, max_commits=300):
        try:
            repo = Repo(repo_path)
            git = repo.git

            # --- BƯỚC 1: Lấy dữ liệu thô từ git log ---
            # Sử dụng format đặc biệt để dễ parse:
            # %H: Hash, %P: Parents, %an: Author Name, %ae: Email, %at: Timestamp, %s: Subject, %D: Refs (Branch names)
            # --name-status: Để lấy list file thay đổi
            separator = "|||"
            log_format = f"COMMIT{separator}%H{separator}%P{separator}%an{separator}%ae{separator}%at{separator}%s{separator}%D"

            # Chạy lệnh git log
            # --all: Lấy tất cả nhánh (local + remote)
            # --date-order: Sắp xếp ưu tiên thời gian (datetime) nhưng vẫn giữ cấu trúc cha-con để vẽ graph.
            # Khác với --topo-order (ưu tiên gom nhánh), --date-order xen kẽ các nhánh dựa trên thời gian thực.
            raw_log = git.log(
                branch,
                "--date-order",
                f"--pretty=format:{log_format}",
                "--name-status",
                f"-n {max_commits}"
            )

            # --- BƯỚC 2: Parse dữ liệu ---
            commits = []
            commit_map = {}  # Để truy cập nhanh theo Hash
            current_commit = None

            lines = raw_log.split('\n')

            for line in lines:
                if not line.strip(): continue

                if line.startswith(f"COMMIT{separator}"):
                    # Đây là dòng bắt đầu 1 commit mới
                    parts = line.split(separator)
                    if len(parts) >= 8:
                        hexsha = parts[1]
                        parents_str = parts[2]
                        author_name = parts[3]
                        author_email = parts[4]
                        timestamp = int(parts[5])
                        subject = parts[6]
                        refs_str = parts[7]

                        parents = parents_str.split() if parents_str else []

                        # Xử lý Refs để tìm branch potential
                        # refs_str ví dụ: "HEAD -> main, origin/main, origin/feature/abc"
                        refs = []
                        if refs_str:
                            # Tách các ref, loại bỏ 'HEAD -> '
                            raw_refs = [r.strip() for r in refs_str.split(',')]
                            for r in raw_refs:
                                clean_ref = r.replace('HEAD -> ', '')
                                if clean_ref != 'HEAD':  # Bỏ qua HEAD pointer
                                    refs.append(clean_ref)

                        current_commit = {
                            "id": hexsha,
                            "parents": parents,
                            "author": {
                                "name": author_name,
                                "email": author_email,
                                "initials": GitService.get_initials(author_name)
                            },
                            "date": datetime.datetime.fromtimestamp(timestamp).isoformat(),
                            "message": subject,
                            "refs": refs,
                            "changes": [],
                            "branch": None  # Sẽ tính sau
                        }
                        commits.append(current_commit)
                        commit_map[hexsha] = current_commit

                elif current_commit and line[0] in ['M', 'A', 'D', 'R', 'C', 'U']:
                    # Đây là dòng file change (VD: "M    src/app.js")
                    # Parse theo tab hoặc space
                    parts = re.split(r'\s+', line.strip(), maxsplit=1)
                    if len(parts) == 2:
                        status_char = parts[0][0]  # Lấy ký tự đầu (M, A, D...)
                        file_path = parts[1]
                        current_commit["changes"].append({
                            "file": file_path,
                            "status": status_char
                        })

            # --- BƯỚC 3: Gán Branch (Branch Coloring Strategy) ---
            # Thuật toán:
            # 1. Xác định các "đầu nhánh" (Tips) dựa vào refs.
            # 2. Ưu tiên các nhánh Main (master/main/develop) đi trước.
            # 3. Trace ngược từ Tip về quá khứ theo Parent[0] (First Parent).
            # 4. Nếu commit đã có branch thì dừng (để nhánh phụ không ghi đè nhánh chính).

            # 3.1 Tìm tất cả các Tips
            tips = []  # List tuple (branch_name, commit_hash)

            # Các từ khóa ưu tiên
            PRIORITY_KEYWORDS = ['main', 'master', 'develop', 'release', 'production']

            for commit in commits:
                if commit["refs"]:
                    # Lấy ref đầu tiên làm đại diện (ưu tiên local trước nếu có)
                    # Sắp xếp refs của commit này để chọn cái tên "đẹp nhất"
                    # Ví dụ: ưu tiên 'main' hơn 'origin/main'
                    best_ref = commit["refs"][0]
                    for ref in commit["refs"]:
                        if not ref.startswith('origin/'):
                            best_ref = ref
                            break

                    tips.append((best_ref, commit["id"]))

            # 3.2 Sắp xếp độ ưu tiên xử lý Tips
            def tip_sort_key(item):
                ref_name = item[0].lower()
                short_name = ref_name.split('/')[-1]

                # Nhóm 1: Main/Master/Develop (Ưu tiên cao nhất để vẽ trục thẳng)
                if any(kw == short_name for kw in PRIORITY_KEYWORDS):
                    return 0
                if any(kw in short_name for kw in PRIORITY_KEYWORDS):
                    return 1
                # Nhóm 2: Feature/Fix
                return 2

            tips.sort(key=tip_sort_key)

            # 3.3 Trace ngược (Back-propagation)
            for branch_name, start_hash in tips:
                curr_hash = start_hash

                while curr_hash in commit_map:
                    commit_obj = commit_map[curr_hash]

                    # Nếu commit này đã được gán branch bởi luồng ưu tiên hơn -> Dừng
                    if commit_obj["branch"] is not None:
                        break

                    # Gán branch
                    commit_obj["branch"] = branch_name

                    # Di chuyển về cha đầu tiên (First Parent)
                    # Đây là chìa khóa để giữ "thẳng hàng" cho nhánh
                    if commit_obj["parents"]:
                        curr_hash = commit_obj["parents"][0]
                    else:
                        break  # Root commit

            # 3.4 Cleanup & Finalize
            # Những commit nào vẫn chưa có branch (do nằm lơ lửng hoặc detached), gán tạm
            for commit in commits:
                if commit["branch"] is None:
                    commit["branch"] = "detached"

                # Xác định type
                commit["type"] = "merge" if len(commit["parents"]) > 1 else "commit"

                # Clean up field không cần thiết gửi về FE
                del commit["refs"]

            return commits

        except Exception as e:
            print(f"Error parsing git log: {str(e)}")
            # Trả về mảng rỗng hoặc lỗi để FE xử lý
            return []

    @staticmethod
    def open_repo(repo_path):
        try:
            # 1. Open Repo
            # pygit2 sẽ raise pygit2.GitError nếu path không hợp lệ
            repo = pygit2.Repository(repo_path)

            # Lấy tên repo (tên folder)
            name = os.path.basename(repo_path)

            # --------------------------
            # 2. Check Status (Clean/Dirty)
            # --------------------------
            # pygit2.Repository.status() trả về dict {filepath: flags}
            # Nếu dict rỗng tức là clean.
            status_entries = repo.status()
            status = "clean" if not status_entries else "dirty"

            # --------------------------
            # 3. Detect Current Branch
            # --------------------------
            if repo.head_is_detached:
                current_branch = "DETACHED"
            else:
                # repo.head là một Reference, shorthand sẽ trả về tên ngắn gọn (ví dụ: main)
                current_branch = repo.head.shorthand

            # --------------------------
            # 4. Detect default branch
            # --------------------------
            default_branch = None
            try:
                # Cố gắng tìm symbolic ref của origin/HEAD
                origin_head = repo.references.get("refs/remotes/origin/HEAD")
                if origin_head and origin_head.type == pygit2.GIT_REF_SYMBOLIC:
                    # Target thường là 'refs/remotes/origin/main', ta cắt lấy phần cuối
                    default_branch = origin_head.target.split('/')[-1]
                else:
                    # Raise lỗi để nhảy xuống catch fallback
                    raise Exception("No symbolic ref")
            except:
                # Fallback: kiểm tra branch local xem có main hay master không
                local_branch_names = list(repo.branches.local)
                default_branch = "main" if "main" in local_branch_names else "master"

            # --------------------------
            # 5. List Branches
            # --------------------------
            local_branches = list(repo.branches.local)

            # Lấy danh sách remote branches (vd: origin/main)
            remote_branches = list(repo.branches.remote)

            # --------------------------
            # 6. Sort function (Giữ nguyên logic của bạn)
            # --------------------------
            local_branches = GitService.sort_branches(local_branches, default_branch)
            remote_branches = GitService.sort_branches(remote_branches, default_branch)

            # --------------------------
            # 7. Changed Files & Untracked
            # --------------------------
            changed_files = []

            # pygit2.status() trả về tất cả thay đổi (Staged, Unstaged, Untracked) trong cùng 1 dict
            # Ta cần phân loại để sắp xếp Untracked xuống cuối giống logic cũ nếu muốn,
            # hoặc duyệt qua và xử lý luôn. Dưới đây tách ra để dễ kiểm soát.

            diff_entries = []
            untracked_entries = []

            for filepath, flags in status_entries.items():
                entry_data = {
                    "id": 0,  # Sẽ điền sau
                    "name": os.path.basename(filepath),
                    "path": os.path.dirname(filepath).replace('/', '\\'),
                    "type": os.path.splitext(filepath)[1][1:]
                }

                # Kiểm tra cờ trạng thái để xem là Untracked (New) hay Modified
                if flags & pygit2.GIT_STATUS_WT_NEW:
                    untracked_entries.append(entry_data)
                else:
                    # Bao gồm Modified, Deleted, Renamed...
                    diff_entries.append(entry_data)

            # Gán ID (Diff trước, Untracked sau giống code cũ)
            file_id = 1
            for item in diff_entries:
                item['id'] = file_id
                changed_files.append(item)
                file_id += 1

            for item in untracked_entries:
                item['id'] = file_id
                changed_files.append(item)
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

        except pygit2.GitError as e:
            # Xử lý lỗi đặc thù của pygit2 (repo không tồn tại, lỗi quyền...)
            # Nếu muốn bắt chính xác lỗi "Invalid repo", pygit2 thường ném GitError khi init Repository
            if "Repository not found" in str(e) or "could not find repository" in str(e).lower():
                raise Exception(f"Invalid Git repo: {repo_path}")
            raise Exception(f"Git error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")