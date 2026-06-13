import sqlite3
from pathlib import Path

db_path=(Path(__file__).parent.parent.parent / "data" / "inventory.db")

def check_inventory(sku:str):
    conn=sqlite3.connect(db_path)
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()

    cursor.execute("""SELECT * FROM products WHERE sku = ?""", (sku,))

    row=cursor.fetchone()
    conn.close()

    if not row:

        return {
            "found": False,
            "message": (
                f"SKU {sku} not found"
            )
        }

    return {
        "found": True,
        "product": dict(row)
    }

