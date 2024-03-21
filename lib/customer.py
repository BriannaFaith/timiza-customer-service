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

cursor.execute ("""
CREATE TABLE IF NOT EXISTS tickets(
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    subject TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'open',
    assigned_staff INTEGER,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
""")

class Customer:
    def __init__(self, id, username, password_hash, email, first_name, last_name, phone_number, address):
        self.id = id
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
        cursor.execute("SELECT id, * FROM customers WHERE username = ? AND password_hash = ?", (username, password))
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

    def create_ticket(self):
        subject = input("Enter the ticket subject: ")
        description = input("Enter a brief description: ")
        priority = input("Choose priority (low, medium, high): ").lower()
        status = 'open'  # Status is set to 'open' by default
        assigned_staff = None
        try:
            cursor.execute("""
                INSERT INTO tickets (customer_id, subject, description, priority, status, assigned_staff)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.id, subject, description, priority, status, assigned_staff))
            conn.commit()
            print("New ticket created successfully.")
        except sqlite3.IntegrityError:
            print("Error: Failed to create ticket.")

    def delete_ticket(self, ticket_id):
        try:
            cursor.execute("DELETE FROM tickets WHERE ticket_id = ? AND customer_id = ?", (ticket_id, self.id))
            conn.commit()
            print("Ticket deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting ticket: {e}")

    def show_tickets(self):
        tickets = Tickets.get_tickets_by_customer_id(self.id)
        if tickets:
            print("Tickets: ")
            for ticket in tickets:
                print("----------")
                print(f"Ticket ID: {ticket[0]}")
                print(f"Subject: {ticket[2]}")
                print(f"Description: {ticket[3]}")
                print(f"Priority: {ticket[4]}")
                print(f"Status: {ticket[5]}")
                print(f"Assigned Staff: {ticket[6]}")
                print(f"Date: {ticket[7]}")
                print("----------")
        else:
            print("You have no tickets")


class Tickets:
    def __init__(self, customer_id, subject, description, priority, status, assigned_staff, creation_date ):
        self.customer_id = customer_id
        self.subject= subject
        self.description= description
        self.priority = priority
        self.status = status
        self.assigned_staff = assigned_staff
        self.creation_date = creation_date

    def save(self):
        """Save the ticket data to the database."""
        try:
            cursor.execute("""
                INSERT INTO tickets (customer_id, subject, description, priority, status, assigned_staff, creation_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.customer_id, self.subject, self.description, self.priority, self.status,self.assigned_staff, self.creation_date))
            conn.commit()
            print("New ticket created successfully.")

        except sqlite3.IntegrityError:
            print("Error: Failed to create ticket.")

    @staticmethod
    def get_tickets_by_customer_id(customer_id):
        """Retrieve all tickets for a specific customer."""
        cursor.execute("SELECT * FROM tickets WHERE customer_id = ?", (customer_id,))
        return cursor.fetchall()



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
    2 - Tickets
    3 - Submit feedback
    4 - Generate Report
    5 - Exit
    '''
    tickets_options = '''
    0 - Show tickets
    1 - Create a ticket
    2 - Delete a ticket
    3 - Go back
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
                        print(tickets_options)
                        while True:
                            tickets_option = input('Ticket Options >> ')
                            if tickets_option == '0':
                                customer.show_tickets()
                                print(tickets_options)
                            elif tickets_option == '1':
                                customer.create_ticket()
                            elif tickets_option == '2':
                                ticket_id = input("Enter the ticket id to delete: ")
                                customer.delete_ticket(ticket_id)
                            elif tickets_option == '3':
                                break

                            else:
                                print("Invalid option")

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
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            username = input("Enter your preffered username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            phone_number = input("Enter phone number: ")
            address = input("Enter address: ")

            new_customer = Customer(None, username, hashlib.sha256(password.encode()).hexdigest(), email, first_name, last_name, phone_number, address)
            new_customer.save()
            print("Account created successfully.")
        elif selectOption == '2':
            print("Customer support")
        elif selectOption == '3':
            exit()
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()
