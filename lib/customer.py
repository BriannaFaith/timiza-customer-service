import sqlite3
import hashlib

conn = sqlite3.connect("timiza-data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    email TEXT,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT,
    address TEXT
)
""")

class Customer:
    def __init__(self, username, password_hash, email, first_name, last_name, phone_number, address):
        self.username = username
        self.password_hash = password_hash
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

    @staticmethod
    def sign_in():
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        cursor.execute("SELECT * FROM customers WHERE username = ? AND password_hash = ?", (username, password))
        customer_data = cursor.fetchone()

        if customer_data:
            return Customer(*customer_data[1:])
        else:
            print("Invalid username or password.")

    def show_account_info(self):
        cursor.execute("SELECT * FROM customers WHERE username = ?", (self.username,))
        customer_data = cursor.fetchone()

        if customer_data:
            print(f"First Name: {customer_data[4]}")
            print(f"Last Name: {customer_data[5]}")
            print(f"Username: {customer_data[1]}")
            print(f"Email Address: {customer_data[3]}")
            print(f"Phone Number: {customer_data[6]}")
            print(f"Location: {customer_data[7]}")
            print (f"Password: {customer_data[2]}")

        else:
            print("Customer not found in the database.")


    def update_account_information(self,password, email, first_name, last_name, phone_number, address):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute("UPDATE customers SET password_hash = ?, email = ?, first_name = ?, last_name = ?, phone_number = ?, address = ? WHERE username = ?",
                           (self.password_hash, self.email, self.first_name, self.last_name, self.phone_number, self.address, self.username))
            conn.commit()
            print("Account information updated successfully.")
        except sqlite3.IntegrityError:
            print("Error: Failed to update account information.")

def main():
    options = '''
    0 - Sign in
    1 - Create a new account
    2 - Customer Support
    3 - Exit
    '''
    print(options)

    account_options = '''
    0 - Account Information
    1 - Update account Information
    2 - Create a ticket
    3 - Submit feedback
    4 - Generate Report
    5 - Exit
    '''

    while True:
        selectOption = input('Option >> ')
        if selectOption == '0':
            customer = Customer.sign_in()
            if customer:
                print(account_options)
                while True:
                    account_option = input('Account Options >> ')
                    if account_option == '0':
                        customer.show_account_info()
                        print(account_options)
                    elif account_option == '1':
                        password= input ("Enter new password:")
                        email = input("Enter new email: ")
                        first_name = input("Enter new first name: ")
                        last_name = input("Enter new last name: ")
                        phone_number = input("Enter new phone number: ")
                        address = input("Enter new address: ")
                        customer.update_account_information(password, email, first_name, last_name, phone_number, address)
                    elif account_option == '2':
                        print("Creates a new ticket")
                    elif account_option == '3':
                        print("Submit feedback")
                    elif account_option == '4':
                        print("Generating report")
                    elif account_option == '5':
                        print(options)
                        break
                    else:
                        print("Invalid option")
        elif selectOption == '1':
            # Implement account creation logic here
            print("Account creation not implemented yet")
        elif selectOption == '2':
            print("Customer support")
        elif selectOption == '3':
            exit()
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()
