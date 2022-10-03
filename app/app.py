import os

import mysql.connector
from flask import Flask
from mysql.connector import Error

app = Flask(__name__)

MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "mysql")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")


@app.route("/")
def index():
    message = ""
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST, database=MYSQL_DATABASE, user=MYSQL_USER, password=MYSQL_PASSWORD
        )

        if connection.is_connected():
            db_Info = connection.get_server_info()
            message = f"Connected to MySQL Server version {db_Info}\n"
            cursor = connection.cursor()
            cursor.execute("SELECT database();")
            record = cursor.fetchone()
            message += f"Connected to database: {record}\n"

    except Error as e:
        message = f"Error connecting to MySQL: {e}"

    return message


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181, debug=True)
