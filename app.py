from flask import Flask
from urllib.parse import unquote, urlparse

import pymysql

from extension import db


def ensure_database_exists(database_uri):
    parsed_uri = urlparse(database_uri)
    database_name = parsed_uri.path.lstrip("/")

    if not database_name:
        return

    connection = pymysql.connect(
        host=parsed_uri.hostname or "localhost",
        user=unquote(parsed_uri.username) if parsed_uri.username else None,
        password=unquote(parsed_uri.password) if parsed_uri.password else "",
        port=parsed_uri.port or 3306,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.commit()
    finally:
        connection.close()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret1234'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/db_tareas"
# initialize the app with the extension
ensure_database_exists(app.config["SQLALCHEMY_DATABASE_URI"])
db.init_app(app)
from models import Tarea
with app.app_context():
    db.create_all()
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
    
