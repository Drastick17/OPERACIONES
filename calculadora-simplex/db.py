import sqlite3

class DatabaseManager:
    def __init__(self):
        self.connection = self.set_connection()
        self.create_table_users()
        self.create_default_users()

    def set_connection(self):
        connection = sqlite3.connect('./database.db')
        return connection

    def create_table_users(self):
        query = '''
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            );
        '''
        with self.connection:
            self.connection.execute(query)

    def create_default_users(self):
        users = [
            ('Ariel', '123py'),
            ('Danny', '123py'),
            ('Robinson', '123py'),
            ('', '')
        ]
        query = "INSERT INTO USERS (name, password) VALUES (?, ?)"
        with self.connection:
            self.connection.executemany(query, users)

    def validate_user(self, name, password):
        query = 'SELECT * FROM USERS WHERE NAME = ? AND PASSWORD = ?'
        with self.connection:
            cursor = self.connection.execute(query, (name, password))
            user = cursor.fetchone()
            if user:
                return True
            return False
        
    def register_user(self, name, repeat_password, password):
        query = "INSERT INTO USERS (name, password) VALUES (?, ?)"
        with self.connection:
            try:
                print(password, repeat_password)
                if repeat_password == password:
                    self.connection.execute(query, (name, password))
                    return 'create'
                else:
                    return 'no same'
            except:
                return 'error'
