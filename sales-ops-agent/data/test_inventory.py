import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "inventory.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM products"
)

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()