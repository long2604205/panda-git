import os

import pygit2


class RepositoryService:
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
            local_branches = RepositoryService.sort_branches(local_branches, default_branch)
            remote_branches = RepositoryService.sort_branches(remote_branches, default_branch)

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
