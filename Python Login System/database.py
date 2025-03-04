import sqlite3
import hashlib

class Database:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                security_question TEXT,
                security_answer TEXT
            )"""
        )
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, security_question, security_answer):
        try:
            hashed_pw = self.hash_password(password)
            self.cursor.execute(
                "INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)",
                (username, hashed_pw, security_question, security_answer)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def get_security_question(self, username):
        self.cursor.execute("SELECT security_question FROM users WHERE username=?", (username,))
        return self.cursor.fetchone()

    def validate_security_answer(self, username, answer):
        self.cursor.execute("SELECT security_answer FROM users WHERE username=?", (username,))
        stored_answer = self.cursor.fetchone()
        return stored_answer and stored_answer[0] == answer

    def update_password(self, username, new_password):
        hashed_pw = self.hash_password(new_password)
        self.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_pw, username))
        self.conn.commit()
