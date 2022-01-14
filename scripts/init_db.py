from sqlite3 import connect
from src.utils import Types


connection = connect("./src/assets/klixx.sqlite")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS types (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, value TEXT UNIQUE NOT NULL);"
)
cursor.executemany("INSERT INTO types VALUES (?, ?);", [(None, t.value) for t in Types])
connection.commit()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS klixx (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, data TEXT NOT NULL, type INTEGER NOT NULL, created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(type) REFERENCES types(id));"
)
connection.commit()

connection.close()
