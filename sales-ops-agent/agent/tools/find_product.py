import sqlite3
from pathlib import Path

db_path=Path(__file__).parent.parent.parent / "data" / "inventory.db"

def find_product(keyword:str):

    conn=sqlite3.connect(db_path)
    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()

    cursor.execute("""
SELECT * FROM products WHERE LOWER(name) LIKE (?)
""", (f"%{keyword}%"))

    rows=cursor.fetchall()

    conn.close()

    return {
        "matches": [
            dict(row)
            for row in rows
        ]
    }