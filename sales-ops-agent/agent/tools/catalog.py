import sqlite3

from pathlib import Path


DB_PATH = (
    Path(__file__).parent.parent.parent
    / "data"
    / "inventory.db"
)


def list_inventory():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            sku,
            name,
            quantity,
            unit_price
        FROM products
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return {
        "products": [
            dict(row)
            for row in rows
        ]
    }