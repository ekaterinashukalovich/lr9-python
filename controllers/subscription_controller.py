def get_user_subscriptions(conn, user_id):
    """
    Возвращает валюты, на которые подписан пользователь
    """
    cur = conn.cursor()
    sql = """
        SELECT c.*
        FROM user_currency uc
        JOIN currency c ON c.id = uc.currency_id
        WHERE uc.user_id = ?
    """
    cur.execute(sql, (user_id,))
    rows = cur.fetchall()
    return [dict(r) for r in rows]


def add_subscription(conn, user_id, currency_id):
    cur = conn.cursor()
    sql = "INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)"
    cur.execute(sql, (user_id, currency_id))
    conn.commit()
    return cur.lastrowid


def remove_subscription(conn, user_id, currency_id):
    cur = conn.cursor()
    sql = """
        DELETE FROM user_currency 
        WHERE user_id = ? AND currency_id = ?
    """
    cur.execute(sql, (user_id, currency_id))
    conn.commit()
    return cur.rowcount > 0