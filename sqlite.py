import sqlite3

# CONNECTION

try:
    def setConnection():
        connection = sqlite3.connect('sqlite.db')
        cursor = connection.cursor()

        # CREATE TABLE

        users_table = '''
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL
            );
        '''

        # CREATE DEFAULT ADMINS
        
        users = [
            ('Ariel', '123py'),
            ('Danny', '123py'),
            ('Robinson', '123py'),
            ('a', 'a')
        ]

        users_query = "INSERT INTO USERS (name, password) VALUES (?, ?)"

        cursor.execute(users_table)
        cursor.executemany(users_query, users)
        return cursor

    # QUERYS

    def validate_user(cursor, name, password):
        query = 'SELECT * FROM USERS WHERE NAME = ? AND PASSWORD = ?'
        cursor.execute(query, (name, password))
        user = cursor.fetchone()
        if user:
            return True
        return False

except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
