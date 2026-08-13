import os
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

    Works both locally and on Render.
    """

    try:

        # =================================================
        # Determine SSL certificate location
        # =================================================

        render_ca = "/etc/secrets/ca.pem"

        local_ca = os.getenv(
            "MYSQL_SSL_CA",
            "ca.pem"
        )


        if os.path.exists(render_ca):

            # Running on Render
            ssl_config = {
                "ca": render_ca
            }

        elif os.path.exists(local_ca):

            # Running locally
            ssl_config = {
                "ca": local_ca
            }

        else:

            print(
                "WARNING: SSL CA certificate not found."
            )

            ssl_config = None


        # =================================================
        # Connect to MySQL
        # =================================================

        connection = pymysql.connect(

            host=DB_HOST,

            port=DB_PORT,

            user=DB_USER,

            password=DB_PASSWORD,

            database=DB_NAME,

            cursorclass=pymysql.cursors.DictCursor,

            ssl=ssl_config
        )


        print(
            "Successfully connected to MySQL."
        )

        return connection


    except pymysql.MySQLError as e:

        print(
            f"Database Connection Error: {e}"
        )

        return None