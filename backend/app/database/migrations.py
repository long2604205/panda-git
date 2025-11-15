import duckdb
import os
from app.utils.environment import getenv


def migrate():
    # Đường dẫn file DB
    db_folder = getenv("DUCKDB_FOLDER")
    db_name = getenv("DUCKDB_NAME")

    os.makedirs(db_folder, exist_ok=True)  # tạo folder nếu chưa có
    db_path = os.path.join(db_folder, db_name)

    # Kết nối DB file
    con = duckdb.connect(db_path)

    # Tạo bảng schema_version nếu chưa có
    con.execute("""
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER
    )
    """)

    # Nếu chưa có record version nào, chèn version 0
    res = con.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0]
    if res == 0:
        con.execute("INSERT INTO schema_version (version) VALUES (0)")

    # Lấy version hiện tại
    current_version = con.execute("SELECT version FROM schema_version").fetchone()[0]

    # Migration v1: tạo bảng repositories
    if current_version < 1:
        con.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            path VARCHAR,
            status VARCHAR,
            active BOOLEAN DEFAULT FALSE
        )
        """)
        con.execute("UPDATE schema_version SET version = 1")
        print("Migration v1 applied: repositories table created.")
    else:
        print("DB already at version >= 1")