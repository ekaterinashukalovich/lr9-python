import sqlite3

def get_connection():
    """Создаёт подключение к базе SQLite в памяти."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    cur = conn.cursor()

    # Таблица пользователей
    cur.execute("""
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    # Таблица валют
    cur.execute("""
        CREATE TABLE currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT NOT NULL,
            char_code TEXT NOT NULL,
            name TEXT NOT NULL,
            value FLOAT,
            nominal INTEGER
        )
    """)

    # Таблица подписок
    cur.execute("""
        CREATE TABLE user_currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            currency_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(currency_id) REFERENCES currency(id)
        )
    """)

    conn.commit()