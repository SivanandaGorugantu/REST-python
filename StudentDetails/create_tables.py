import sqlite3

connection = sqlite3.connect("studentDB.db")
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS students (name text, CGPA text)"
cursor.execute(create_table)

#cursor.execute("INSERT INTO students VALUES ('test',4.0)")

connection.commit()

connection.close()