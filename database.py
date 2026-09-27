import sqlite3
from pathlib import Path
from datetime import datetime

DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "finance.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            description TEXT,
            transaction_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month TEXT NOT NULL,
            UNIQUE(category, month)
        )
    """)

    conn.commit()
    conn.close()


def add_transaction(
    transaction_type,
    category,
    amount,
    payment_method,
    description,
    transaction_date
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO transactions
        (transaction_type, category, amount, payment_method,
         description, transaction_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transaction_type,
        category,
        amount,
        payment_method,
        description,
        transaction_date
    ))

    conn.commit()
    conn.close()


def get_transactions():
    conn = get_connection()

    query = """
        SELECT
            id,
            transaction_type,
            category,
            amount,
            payment_method,
            description,
            transaction_date
        FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """

    import pandas as pd

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def delete_transaction(transaction_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()
    conn.close()


def add_budget(category, amount, month):
    conn = get_connection()

    conn.execute("""
        INSERT INTO budgets (category, amount, month)
        VALUES (?, ?, ?)
        ON CONFLICT(category, month)
        DO UPDATE SET amount = excluded.amount
    """, (category, amount, month))

    conn.commit()
    conn.close()


def get_budgets(month=None):
    conn = get_connection()

    if month:
        query = """
            SELECT id, category, amount, month
            FROM budgets
            WHERE month = ?
            ORDER BY category
        """

        import pandas as pd

        df = pd.read_sql_query(
            query,
            conn,
            params=(month,)
        )
    else:
        import pandas as pd

        df = pd.read_sql_query(
            "SELECT * FROM budgets ORDER BY month DESC",
            conn
        )

    conn.close()

    return df


def delete_budget(budget_id):
    conn = get_connection()

    conn.execute(
        "DELETE FROM budgets WHERE id = ?",
        (budget_id,)
    )

    conn.commit()
    conn.close()