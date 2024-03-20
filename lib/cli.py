import sqlite3

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

        cursor.execute("INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)",
                       (self.username, self.password_hash, self.role, self.email))
        conn.commit()
    def create_new_user(self):
        pass
    

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
    def __init__(self, type, data):
        self.type = type
        self.data = data

    def save(self):

        cursor.execute("INSERT INTO reports (type, data) VALUES (?, ?)",
                       (self.type, self.data))
        conn.commit()
