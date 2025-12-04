def get_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    return [dict(r) for r in rows]


def get_user_by_id(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    row = cur.fetchone()
    return dict(row) if row else None
