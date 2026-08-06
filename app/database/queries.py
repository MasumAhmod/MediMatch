from app.database.db import get_connection

# ................get_all_doctors
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

#............get_doctor_by_id
def get_doctor_by_id(doctor_id: int):
    """
    Returns a doctor by ID.
    """

    connection = get_connection()

    if connection is None:
        return None

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT *
                FROM doctors
                WHERE doctor_id = %s
                AND is_active = 1
            """

            cursor.execute(sql, (doctor_id,))

            doctor = cursor.fetchone()

            return doctor

    finally:
        connection.close()

# ...........get_doctors_by_name
def search_doctors(
    name=None,
    specialization=None
):
    """
    Search doctors by name and/or specialization.
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

            params = []

            if name:
                sql += " AND doctor_name LIKE %s"
                params.append(f"%{name}%")

            if specialization:
                sql += " AND specialization = %s"
                params.append(specialization)

            cursor.execute(sql, tuple(params))

            doctors = cursor.fetchall()

            return doctors

    finally:
        connection.close()


# ...........filter_doctors
def filter_doctors(
    city=None,
    specialization=None,
    min_fee=None,
    max_fee=None,
    availability=None
):
    """
    Filter doctors based on given criteria.
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

            params = []

            if city:
                sql += " AND city = %s"
                params.append(city)

            if specialization:
                sql += " AND specialization = %s"
                params.append(specialization)

            if min_fee is not None:
                sql += " AND appointment_fee >= %s"
                params.append(min_fee)

            if max_fee is not None:
                sql += " AND appointment_fee <= %s"
                params.append(max_fee)

            if availability is not None:
                sql += " AND availability = %s"
                params.append(availability)

            cursor.execute(sql, tuple(params))

            doctors = cursor.fetchall()

            return doctors

    finally:
        connection.close()



# ...........get_all_specializations
def get_all_specializations():
    """
    Returns all active specializations.
    """

    connection = get_connection()

    if connection is None:
        return []

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT *
                FROM specializations
                WHERE is_active = 1
                ORDER BY specialization
            """

            cursor.execute(sql)

            specializations = cursor.fetchall()

            return specializations

    finally:
        connection.close()


# ...........get_specialization_by_id
def get_specialization_by_id(specialization_id: int):
    """
    Returns a specialization by ID.
    """

    connection = get_connection()

    if connection is None:
        return None

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT *
                FROM specializations
                WHERE id = %s
                AND is_active = 1
            """

            cursor.execute(sql, (specialization_id,))

            specialization = cursor.fetchone()

            return specialization

    finally:
        connection.close()


# ...........search_specializations
def search_specializations(name: str):
    """
    Search specialization by name.
    """

    connection = get_connection()

    if connection is None:
        return []

    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT *
                FROM specializations
                WHERE specialization LIKE %s
                AND is_active = 1
                ORDER BY specialization
            """

            cursor.execute(sql, (f"%{name}%",))

            specializations = cursor.fetchall()

            return specializations

    finally:
        connection.close()