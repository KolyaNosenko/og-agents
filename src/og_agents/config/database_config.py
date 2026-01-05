import os
from pathlib import Path

class DatabaseConfig:
    file_name: str
    file_path: str

    def __init__(self):
        self.file_name = os.environ.get("DATABASE_FILE_NAME")

        root = Path(__file__).resolve().parents[1]
        db_path = root / "db"
        # db_path.mkdir(exist_ok=True)

        self.file_path = os.path.join(db_path, self.file_name)
