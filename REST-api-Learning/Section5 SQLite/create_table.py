import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# Must be tuple
users = [
    ('weber', 'asdf'),
    ('lawrence', 'asdf'),
    ('eva', '1234'),
    ('penny', '1234'),
    ('sabrina', '1234')
]
insert_query = "INSERT INTO users VALUES (NULL, ?, ?)"
cursor.executemany(insert_query, users)

create_table = "CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)"
cursor.execute(create_table)

connection.commit()

connection.close()