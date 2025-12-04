from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader
from models.author import Author
from db import get_connection, init_db

from controllers.currency_controller import (
    get_all_currencies, add_currency, get_currency_by_id,
    update_currency_value, update_currency_by_char_code,
    delete_currency, show_all_currencies_console
)
from controllers.user_controller import (
    get_all_users, get_user_by_id
)
from controllers.subscription_controller import (
    get_user_subscriptions
)

env = Environment(loader=FileSystemLoader("templates"))
conn = get_connection()
init_db(conn)

conn.execute("INSERT INTO user (name) VALUES ('Алиса')")
conn.execute("INSERT INTO user (name) VALUES ('Евгений')")
conn.execute("INSERT INTO user (name) VALUES ('Андрей')")
conn.commit()

author = Author("Ekaterina Shukalovich", "P3121")

class MyHandler(BaseHTTPRequestHandler):

    def show(self, filename, **params):
        try:
            tpl = env.get_template(filename)
            html = tpl.render(**params)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        except Exception as e:
            self.send_error(500, f"Template error: {e}")

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        args = parse_qs(url.query)

        # Меню на всех страницах
        menu = [
            {"caption": "Главная", "href": "/"},
            {"caption": "Пользователи", "href": "/users"},
            {"caption": "Курсы валют", "href": "/currencies"},
            {"caption": "Автор проекта", "href": "/author"},
        ]

        # ---------------- Главная ----------------
        if path == "/":
            self.show(
                "index.html",
                navigation=menu,
                myapp="CurrenciesListApp (MVC version)",
                author_name=author.name,
                group=author.group,
                a_variable="Добро пожаловать!"
            )
            return

        # ---------------- Автор ----------------
        if path == "/author":
            self.show("author_project.html",
                      navigation=menu,
                      author_name=author.name,
                      group=author.group)
            return

        # ---------------- Пользователи ----------------
        if path == "/users":
            users = get_all_users(conn)
            self.show("users.html", navigation=menu, users=users)
            return

        # ---------------- Один пользователь ----------------
        if path == "/user":
            if "id" not in args:
                self.show("error.html",
                          navigation=menu,
                          message="Не указан id пользователя")
                return

            user_id = int(args["id"][0])
            user = get_user_by_id(conn, user_id)

            if not user:
                self.show("error.html",
                          navigation=menu,
                          message="Пользователь не найден")
                return

            subs = get_user_subscriptions(conn, user_id)

            self.show("user.html",
                      navigation=menu,
                      user=user,
                      currencies=subs,
                      history=None)
            return


        # --------- READ ---------
        if path == "/currencies":
            currs = get_all_currencies(conn)
            self.show("currencies.html", navigation=menu, currencies=currs)
            return

        # --------- CREATE: форма ---------
        if path == "/currency/add" and not args:
            self.show("currency_add.html", navigation=menu)
            return

        # --------- CREATE: обработка ---------
        if path == "/currency/add" and args:
            try:
                num_code = args["num_code"][0]
                char_code = args["char_code"][0]
                name = args["name"][0]
                value = float(args["value"][0])
                nominal = int(args["nominal"][0])

                add_currency(conn, num_code, char_code, name, value, nominal)
                self.send_response(302)
                self.send_header("Location", "/currencies")
                self.end_headers()
                return

            except Exception as e:
                self.show("error.html", navigation=menu,
                          message="Ошибка добавления: " + str(e))
                return

        # ----------- UPDATE: форма -----------
        if path == "/currency/update" and "id" in args and "value" not in args:
            cid = int(args["id"][0])
            currency = get_currency_by_id(conn, cid)
            if not currency:
                self.show("error.html", navigation=menu, message="Валюта не найдена")
                return

            self.show("currency_edit.html",
                      navigation=menu,
                      currency=currency)
            return

        # ----------- UPDATE: обработка -----------
        if path == "/currency/update" and "value" in args:
            # вариант 1: /currency/update?id=5&value=90
            if "id" in args:
                cid = int(args["id"][0])
                new_value = float(args["value"][0])
                update_currency_value(conn, cid, new_value)

            # вариант 2: /currency/update?USD=90.5
            else:
                char_code = list(args.keys())[0]
                new_value = float(args[char_code][0])
                update_currency_by_char_code(conn, char_code, new_value)

            self.send_response(302)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return

        # ----------- DELETE: форма -----------
        if path == "/currency/delete" and "confirm" not in args:
            cid = int(args["id"][0])
            currency = get_currency_by_id(conn, cid)

            if not currency:
                self.show("error.html", navigation=menu, message="Валюта не найдена")
                return

            self.show("currency_delete.html",
                      navigation=menu,
                      currency=currency)
            return

        # ----------- DELETE: обработка -----------
        if path == "/currency/delete" and "confirm" in args:
            cid = int(args["id"][0])
            delete_currency(conn, cid)

            self.send_response(302)
            self.send_header("Location", "/currencies")
            self.end_headers()
            return

        # ----------- SHOW (для отладки) -----------
        if path == "/currency/show":
            show_all_currencies_console(conn)
            self.show("info.html",
                      navigation=menu,
                      message="Данные валют выведены в консоль сервера.")
            return

        # ---------------- Unknown route ----------------
        self.show("error.html", navigation=menu,
                  message="Страница не найдена")


if __name__ == "__main__":
    print("Server running on http://localhost:8080")
    httpd = HTTPServer(('localhost', 8080), MyHandler)
    httpd.serve_forever()