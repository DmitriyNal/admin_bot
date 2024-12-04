import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()


def initiate_db():
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Users (
           id INTEGER PRIMARY KEY,
           username TEXT NOT NULL,
           email TEXT NOT NULL,
           age INTEGER NOT NULL,
           balance INTEGER NOT NULL
       )
        ''')


def add_user(username, email, age, balance=1000):
    cursor.execute('''
        INSERT INTO Users (username, email, age, balance)
        VALUES (?, ?, ?, ?)
    ''', (username, email, age, balance))
    connection.commit()


def is_included(username):
    cursor.execute('''
        SELECT * FROM Users
        WHERE username = ?
    ''', (username,))
    return cursor.fetchone() is not None


connection.commit()
