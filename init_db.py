import sqlite3

with open("schema.sql") as f:
    schema = f.read()

conn = sqlite3.connect("skill_swap.db")
conn.executescript(schema)
conn.commit()
conn.close()

print("database and tables are created succesfully.")