import sqlite3
conn=sqlite3.connect("blog.db")
cursor= conn.cursor()
cursor.execute("CREATE TABLE posts (title TEXT,description TEXT);")

