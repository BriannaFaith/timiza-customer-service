import sqlite3
import hashlib

# Connection to the database
conn = sqlite3.connect("timiza-data.db")
cursor = conn.cursor()

# Creating tables

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT
    phone_number TEXT,
    address TEXT
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


class Customers:
    def __init__(self, username, password_hash, role, email,first_name, last_name, phone_number, address):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def save(self):
        """Save the user data to the database."""
        try:
            cursor.execute("INSERT INTO customers (username, password_hash, email, first_name, last_name, phone_number, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (self.username, self.password_hash, self.email, self.first_name, self.last_name, self.phone_number, self.address))
            conn.commit()
            print("New Customer saved successfully.")
        except sqlite3.IntegrityError:
            print("Error: Username already exists.")

    def create_new_customer(self, username, password,email,first_name, last_name, phone_number, address ):

        password_hash = self._hash_password(password)
        new_customer = Customers(username, password_hash,email, first_name, last_name, phone_number, address)
        new_customer.save()
        return new_customer

    def check_password(self, password):
        """Check if the provided password matches the user's password."""
        hashed_password = self._hash_password(password)
        return hashed_password == self.password_hash

    def validate_email(self, email):
        return '@' in email and '.' in email

    def _hash_password(self, password):
        """Hash the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def sign_in():
        username = input( " Enter your username:")
        password_hash= input( " Enter your password:")


        conn = sqlite3.connect("timiza-data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM customers WHERE username = ? AND password_hash = ?", (username, password_hash))
        customer = cursor.fetchone()

        if customer:
            print("Sign in successful!")
        else:
            print("Invalid username or password. Try again")

        conn.close()

    def account_information(customer):
        print("Account Information")
        print(f"Username: {customer.username}")
        print(f"Password: {customer.password_hash}")
        print(f"Email: {customer.email}")
        print(f"Full Name: {customer.first_name, customer.last_name}")
        print(f"Phone Number: {customer.phone_number}")
        print(f"Address: {customer.address}")



    #@classmethod
    #def find_by_username(cls, username):
        #"""Find a user by username."""
        #cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        #user_data = cursor.fetchone()
        #if user_data:
            #return cls(*user_data)
        #return None


#class Tickets:
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


#class Categories:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def save(self):
        cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)",
                       (self.name, self.description))
        conn.commit()

#class Reports:
    all_reports = {}

    def __init__(self, type, data):
        self.type = type
        self.data = data

    def save(self):
        cursor.execute("INSERT INTO reports (type, data) VALUES (?, ?)",
                       (self.type, self.data))
        conn.commit()
    @classmethod
    def get_all_reports(cls):
        conn = sqlite3.connect("timiza-data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reports")
        all_reports = cursor.fetchall()
        conn.close()
        return all_reports

def main():
    options = '''
    0 - Sign in
    1 - Create a new account
    2 - Customer Support
    3 - Exit
    '''
    print(options)

    account_options= '''
    0 - Account Information
    1 - Update account Information
    2 - Create a ticket
    3 - Submit feedback
    4 - Generate Report
    5 - Exit
    '''


    while True:
        selectOption = input ('Option >>')
        if selectOption == '0':
            customer = Customers.sign_in()
            if customer:
                print(account_options)
                account_option = input ('Account Options >>')
                if account_option == '0':
                    Customers().account_information(customer)
                elif account_option == '1':
                    print("Updates info")
                elif account_option == '2':
                    print("Creates a new ticket")
                elif account_option == '3':
                    print("Submit feedback")
                elif account_option == '4':
                    print("Generating report")
                elif account_option == '5':
                    exit()
                else:
                    ("Invalid option")
        elif selectOption == '1':
            customer = Customers.create_account()
            if customer:
                account_options(customer)

                return
        elif selectOption == '2':
            print("Customer support")
        elif selectOption == '3':
            exit()
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()
