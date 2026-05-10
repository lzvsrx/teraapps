import sqlite3
import hashlib
import os

class Database:
    def __init__(self, db_name="tera.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                profession TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Files/Data table for professions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT,
                content TEXT,
                file_blob BLOB,
                file_name TEXT,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password, profession):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, profession) VALUES (?, ?, ?)",
                (username, hashed_pw, profession)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login_user(self, username, password):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute(
            "SELECT id, username, profession FROM users WHERE username = ? AND password = ?",
            (username, hashed_pw)
        )
        return self.cursor.fetchone()

    def save_user_data(self, user_id, title, content, category, file_path=None):
        file_blob = None
        file_name = None
        if file_path and os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as f:
                file_blob = f.read()
        
        self.cursor.execute(
            "INSERT INTO user_data (user_id, title, content, category, file_blob, file_name) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, title, content, category, file_blob, file_name)
        )
        self.conn.commit()

    def get_user_data(self, user_id, category=None):
        if category:
            self.cursor.execute("SELECT * FROM user_data WHERE user_id = ? AND category = ?", (user_id, category))
        else:
            self.cursor.execute("SELECT * FROM user_data WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
