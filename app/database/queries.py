from app.database.db import get_connection


def get_all_doctors():
    """
    Returns all active doctors.
    """

    connection = get_connection()

    if connection is None:
        return []

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT *
                FROM doctors
                WHERE is_active = 1
            """

            cursor.execute(sql)

            doctors = cursor.fetchall()

            return doctors

    finally:
        connection.close()