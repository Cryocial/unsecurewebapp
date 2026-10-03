"""
DashDoor — database setup.

Run this once to build dashdoor.db:

    python db.py

It creates three tables (users, menu, orders) and seeds them. Note the
`visible` column on `menu`: items with visible = 0 are the "secret staff
menu" and should NEVER show up in a normal search. (lie)
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashdoor.db")


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # --- users -------------------------------------------------------------
    c.execute("""
        CREATE TABLE users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    """)
    c.executemany(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        [
            ("john",  "intern",       0),
            ("guest",  "guest",         0),
            ("admin",  "DashD00r!2024", 1),   
        ],
    )

    # --- menu --------------------------------------------------------------
    c.execute("""
        CREATE TABLE menu (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            price   REAL NOT NULL,
            visible INTEGER NOT NULL DEFAULT 1
        )
    """)
    c.executemany(
        "INSERT INTO menu (name, price, visible) VALUES (?, ?, ?)",
        [
            ("Classic Burrito",      8.50, 1),
            ("Chicken Tacos (3)",    7.25, 1),
            ("Loaded Fries",         5.00, 1),
            ("Boba Milk Tea",        4.50, 1),
            ("Veggie Bowl",          9.00, 1),
            ("Churros (6)",          4.00, 1),
            ("Staff Meal: Free Boba Forever",   0.00, 0),
            ("Staff Meal: Free Burrito",        0.00, 0),
            ("todo:dlete this code later test discount code = ADMIN100", 0.00, 0),
        ],
    )

    # --- orders ------------------------------------------------------------
    c.execute("""
        CREATE TABLE orders (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            summary  TEXT NOT NULL,
            total    REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print(f"Built {DB_PATH}")


if __name__ == "__main__":
    init_db()
