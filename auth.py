from db import Database
import hashlib


class Auth:

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()
        self.cursor = self.db.get_cursor(self.connection)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def email_exists(self, email):
        query = "SELECT * FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone() is not None

    def register(self):
        print("\n------ Register ------")

        name = input("Enter Full Name : ").strip()
        email = input("Enter Email : ").strip().lower()
        password = input("Enter Password : ").strip()

        if not name or not email or not password:
            print("All fields are required.")
            return

        if self.email_exists(email):
            print("Email already registered.")
            return

        hashed_password = self.hash_password(password)

        query = """
        INSERT INTO users(full_name, email, password)
        VALUES (%s, %s, %s)
        """

        values = (name, email, hashed_password)

        self.cursor.execute(query, values)
        self.connection.commit()

        print("Registration Successful!")
        
    def login(self):

        print("\n------ Login ------")

        email = input("Enter Email : ").strip().lower()

        password = input("Enter Password : ").strip()

        hashed_password = self.hash_password(password)

        query = """
        SELECT id, full_name
        FROM users
        WHERE email=%s
        AND password=%s
        """

        values = (email, hashed_password)

        self.cursor.execute(query, values)

        user = self.cursor.fetchone()

        if user:
            print(f"\nWelcome {user[1]}!")
            return user[0] 
        else:
            return None