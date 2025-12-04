import sqlite3


# -------- CREATE --------
def add_currency(conn, num_code, char_code, name, value, nominal):
    cur = conn.cursor()
    sql = """
        INSERT INTO currency (num_code, char_code, name, value, nominal)
        VALUES (?, ?, ?, ?, ?)
    """
    cur.execute(sql, (num_code, char_code, name, value, nominal))
    conn.commit()
    return cur.lastrowid


# -------- READ --------
def get_all_currencies(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM currency")
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def get_currency_by_id(conn, cid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM currency WHERE id = ?", (cid,))
    row = cur.fetchone()
    return dict(row) if row else None


def get_currency_by_char_code(conn, char_code):
    cur = conn.cursor()
    cur.execute("SELECT * FROM currency WHERE char_code = ?", (char_code,))
    row = cur.fetchone()
    return dict(row) if row else None


# -------- UPDATE  --------
def update_currency_value(conn, cid, new_value):
    cur = conn.cursor()
    sql = "UPDATE currency SET value = ? WHERE id = ?"
    cur.execute(sql, (new_value, cid))
    conn.commit()
    return cur.rowcount > 0


def update_currency_by_char_code(conn, char_code, new_value):
    cur = conn.cursor()
    sql = "UPDATE currency SET value = ? WHERE char_code = ?"
    cur.execute(sql, (new_value, char_code))
    conn.commit()
    return cur.rowcount > 0


# -------- DELETE --------
def delete_currency(conn, cid):
    cur = conn.cursor()
    sql = "DELETE FROM currency WHERE id = ?"
    cur.execute(sql, (cid,))
    conn.commit()
    return cur.rowcount > 0


# -------- SHOW (debug) --------
def show_all_currencies_console(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM currency")
    rows = cur.fetchall()
    print("\n--- Currency table dump ---")
    for r in rows:
        print(dict(r))
    print("--- End dump ---\n")
    return len(rows)