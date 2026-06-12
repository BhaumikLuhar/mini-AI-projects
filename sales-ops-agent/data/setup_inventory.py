import sqlite3
from pathlib import Path

db_path=Path(__file__).parent / "inventory.db"

def setup_database():

    conn=sqlite3.connect(db_path)

    cursor=conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL
                   )
""")
    
    cursor.execute("DELETE FROM products")

    sample_products = [
        (
            "LAPTOP001",
            "Business Laptop",
            25,
            50000
        ),
        (
            "LAPTOP002",
            "Developer Laptop",
            15,
            75000
        ),
        (
            "MONITOR001",
            "27-inch Monitor",
            40,
            12000
        ),
        (
            "KEYBOARD001",
            "Mechanical Keyboard",
            75,
            2500
        ),
        (
            "MOUSE001",
            "Wireless Mouse",
            100,
            1200
        )
    ]

    cursor.executemany(
        """
        INSERT INTO products
        (
            sku,
            name,
            quantity,
            unit_price
        )
        VALUES (?, ?, ?, ?)
        """,
        sample_products
    )

    conn.commit()
    conn.close()

    print(
        "Inventory database created successfully."
    )


if __name__ == "__main__":
    setup_database()