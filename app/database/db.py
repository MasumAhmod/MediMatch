import pymysql


def get_connection():
    """
    Create and return a MySQL database connection.
    """

    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="@Lovedit0",
            database="medimatch",
            cursorclass=pymysql.cursors.DictCursor
        )

        return connection

    except pymysql.MySQLError as e:
        print(f"Database Connection Error: {e}")
        return None