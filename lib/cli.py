import sqlite3
import hashlib

# Connection to the database
conn = sqlite3.connect("timiza-data.db")
cursor = conn.cursor()

# Creating tables

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT,
    email TEXT
)
""")

# Tickets table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    agent_id INTEGER,
    category_id INTEGER,
    status TEXT,
    priority TEXT,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (agent_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
""")

# Categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories(
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT
)
""")

# Reports table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports(
    id INTEGER PRIMARY KEY,
    type TEXT,
    data TEXT,
    generated_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")


class Users:
    def __init__(self, username, password_hash, role, email):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.email = email

    def save(self):
        """Save the user data to the database."""
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                           (self.username, self.password_hash, self.role, self.email))
            conn.commit()
            print("User saved successfully.")
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")

    def create_new_user(self, username, password, role, email):

        password_hash = self._hash_password(password)
        new_user = Users(username, password_hash, role, email)
        new_user.save()
        return new_user

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        hashed_password = self._hash_password(password)
        return hashed_password == self.password_hash

    def validate_email(self, email):
        return '@' in email and '.' in email

    def _hash_password(self, password):
        """Hash the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()


    @classmethod
    def find_by_username(cls, username):
        """Find a user by username."""
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        if user_data:
            return cls(*user_data)
        return None


class Tickets:
    def __init__(self, customer_id, agent_id, category_id, status, priority, description):
        self.customer_id = customer_id
        self.agent_id = agent_id
        self.category_id = category_id
        self.status = status
        self.priority = priority
        self.description = description


    def save(self):

        cursor.execute("INSERT INTO tickets (customer_id, agent_id, category_id, status, priority, description) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.customer_id, self.agent_id, self.category_id, self.status, self.priority, self.description))
        conn.commit()


class Categories:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save(self):
        cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)",
                       (self.name, self.description))
        conn.commit()

class Reports:
    all_reports = { }
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def save(self):
        cursor.execute("INSERT INTO reports (type, data) VALUES (?, ?)",
                       (self.type, self.data))
        conn.commit()

    def get_all_reports():
        conn = sqlite3.connect("timiza-data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports")
        all_reports = cursor.fetchall()
        conn.close()
        return all_reports


if __name__ == "__main__":
    new_user = Users("mitchelle_kwams", "mitch123", "customer", "mitchellekwamboka@gmail.com")
    new_user.save()

    # Check if the password matches
    print(new_user.check_password("mitch123"))


    # Validate an email address
    print(new_user.validate_email("mitchellekwamboka@gmail.com"))

    all_reports = Reports.get_all_reports()
    for report in all_reports:
        print(report)
