import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    c.execute("DROP TABLE IF EXISTS tasks")
    c.execute("""CREATE TABLE tasks
                (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    status INTEGER NOT NULL
                )""")

    tasks = [
                (None, 'Finish this tutorial', "09/22/2016", 10, 1),
                (None, 'Make some delicious pasta', "09/23/2016", 10, 1),
                (None, 'Install updates and shutdown down my computer', "09/24/2016", 8, 1)
            ]
    c.executemany("INSERT INTO tasks VALUES(?,?,?,?,?)", tasks)
