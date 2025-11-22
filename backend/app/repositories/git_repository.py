import duckdb
import hashlib
from datetime import datetime, timezone
from app.utils.environment import getenv
import os

class GitRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_folder = getenv("DUCKDB_FOLDER")
            db_name = getenv("DUCKDB_NAME")
            db_path = os.path.join(db_folder, db_name)

        self.con = duckdb.connect(db_path)

    @staticmethod
    def generate_repo_id(path):
        now = datetime.now(timezone.utc).isoformat()
        s = f"{path}_{now}"
        return hashlib.sha256(s.encode('utf-8')).hexdigest()

    def add_repo(self, name, path, status, active=False):
        id_hash = self.generate_repo_id(path)
        self.con.execute("""
            INSERT INTO repositories (id, name, path, status, active)
            VALUES (?, ?, ?, ?, ?)
        """, (id_hash, name, path, status, active))
        return id_hash

    def update_repo(self, repo_id, name=None, path=None, status=None, active=None):
        """
        Cập nhật thông tin repo theo id.
        Trả về True nếu cập nhật thành công, False nếu repo không tồn tại hoặc không có trường nào để cập nhật.
        """
        updates = []
        params = []

        if name is not None:
            updates.append("name=?")
            params.append(name)
        if path is not None:
            updates.append("path=?")
            params.append(path)
        if status is not None:
            updates.append("status=?")
            params.append(status)
        if active is not None:
            updates.append("active=?")
            params.append(active)

        if not updates:
            print("[INFO] Không có trường nào để cập nhật")
            return False  # Không có gì để update

        # Kiểm tra repo có tồn tại
        exists = self.con.execute(
            "SELECT COUNT(*) FROM repositories WHERE id=?", (repo_id,)
        ).fetchone()[0]

        if not exists:
            print(f"[WARN] Repo {repo_id} không tồn tại trong DB")
            return False

        # Thực hiện update
        sql = f"UPDATE repositories SET {', '.join(updates)} WHERE id=?"
        params.append(repo_id)
        self.con.execute(sql, params)

        print(f"[INFO] Repo {repo_id} updated successfully.")
        return True