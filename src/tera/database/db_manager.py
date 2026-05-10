import sqlite3
import hashlib
import os
from pathlib import Path

class DatabaseManager:
    def __init__(self, app):
        self.app = app
        # Use BeeWare's standard data directory
        data_dir = Path(self.app.paths.data)
        data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = data_dir / "tera.db"
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(str(self.db_path))

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    profession TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS profession_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    content TEXT,
                    data_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, profession):
        hashed_pw = self.hash_password(password)
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password, profession) VALUES (?, ?, ?)",
                    (username, hashed_pw, profession)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        hashed_pw = self.hash_password(password)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, profession FROM users WHERE username = ? AND password = ?",
                (username, hashed_pw)
            )
            return cursor.fetchone()

    def save_profession_data(self, user_id, title, content, data_type):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO profession_data (user_id, title, content, data_type) VALUES (?, ?, ?, ?)",
                (user_id, title, content, data_type)
            )
            conn.commit()

    def get_profession_data(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title, content, data_type, created_at FROM profession_data WHERE user_id = ?",
                (user_id,)
            )
            return cursor.fetchall()
