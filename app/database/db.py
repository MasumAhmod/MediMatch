import pymysql

from config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


def get_connection():
    """
    Create and return a MySQL database connection.
    """

    try:

        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,

            cursorclass=pymysql.cursors.DictCursor,

            ssl={
                "ca": "/etc/secrets/ca.pem"
            }
        )

        return connection

    except pymysql.MySQLError as e:

        print(f"Database Connection Error: {e}")

    return None