import sqlite3
import hashlib
import datetime
import random

class Database:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                security_question TEXT,
                security_answer TEXT,
                email TEXT UNIQUE,
                profile_picture TEXT
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS login_logs (
                id INTEGER PRIMARY KEY,
                username TEXT,
                timestamp TEXT,
                status TEXT
            )
            """
        )
        self.conn.commit()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, security_question, security_answer, email, profile_picture=""):
        try:
            hashed_pw = self.hash_password(password)
            hashed_answer = self.hash_password(security_answer)
            self.cursor.execute("""
                INSERT INTO users (username, password, security_question, security_answer, email, profile_picture)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, hashed_pw, security_question, hashed_answer, email, profile_picture))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username or email already exists

    def validate_user(self, username, password):
        hashed_pw = self.hash_password(password)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
        return self.cursor.fetchone() is not None

    def log_login_attempt(self, username, status):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO login_logs (username, timestamp, status) VALUES (?, ?, ?)", (username, timestamp, status))
        self.conn.commit()

    def get_security_question(self, username):
        self.cursor.execute("SELECT security_question FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def reset_password(self, username, security_answer, new_password):
        hashed_answer = self.hash_password(security_answer)
        self.cursor.execute("SELECT * FROM users WHERE username=? AND security_answer=?", (username, hashed_answer))
        if self.cursor.fetchone():
            hashed_new_pw = self.hash_password(new_password)
            self.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_new_pw, username))
            self.conn.commit()
            return True
        return False
    
    # this is get_user_email method
    def get_user_email(self, username):
        self.cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    def generate_otp(self):
        return random.randint(100000, 999999)

    def update_profile(self, username, new_username=None, new_password=None, new_profile_picture=None):
        if new_username:
            self.cursor.execute("UPDATE users SET username=? WHERE username=?", (new_username, username))
        if new_password:
            hashed_pw = self.hash_password(new_password)
            self.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_pw, username))
        if new_profile_picture:
            self.cursor.execute("UPDATE users SET profile_picture=? WHERE username=?", (new_profile_picture, username))
        self.conn.commit()
        return True
