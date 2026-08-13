from app.database.db import get_connection


# =========================================================
# GET ALL DOCTORS
# =========================================================

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

            return cursor.fetchall()

    finally:

        connection.close()


# =========================================================
# GET DOCTOR BY ID
# =========================================================

def get_doctor_by_id(doctor_id: int):
    """
    Returns an active doctor by ID.
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

            cursor.execute(
                sql,
                (doctor_id,)
            )

            return cursor.fetchone()

    finally:

        connection.close()


# =========================================================
# SEARCH DOCTORS
# =========================================================

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

            # -------------------------------------------------
            # NAME
            # -------------------------------------------------

            if name:

                sql += """
                    AND doctor_name LIKE %s
                """

                params.append(
                    f"%{name}%"
                )

            # -------------------------------------------------
            # SPECIALIZATION
            # -------------------------------------------------

            if specialization:

                from app.utils.specialist import (
                    get_specialization_keywords
                )

                keywords = get_specialization_keywords(
                    specialization
                )

                if keywords:

                    conditions = []

                    for keyword in keywords:

                        conditions.append(
                            "LOWER(specialization) LIKE %s"
                        )

                        params.append(
                            f"%{keyword.lower()}%"
                        )

                    sql += (
                        " AND ("
                        + " OR ".join(conditions)
                        + ")"
                    )

                else:

                    sql += """
                        AND LOWER(specialization) LIKE %s
                    """

                    params.append(
                        f"%{specialization.lower()}%"
                    )

            # -------------------------------------------------
            # ORDER
            # -------------------------------------------------

            sql += """
                ORDER BY doctor_name
            """

            cursor.execute(
                sql,
                tuple(params)
            )

            return cursor.fetchall()

    finally:

        connection.close()


# =========================================================
# FILTER DOCTORS
# =========================================================

def filter_doctors(
    city=None,
    specialization=None,
    min_fee=None,
    max_fee=None,
    availability=None
):
    """
    Filter doctors using optional criteria.

    availability:
        Available / available / 1 -> 1
        Unavailable / unavailable / 0 -> 0
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

            # =================================================
            # CITY
            # =================================================

            if city:

                sql += """
                    AND LOWER(TRIM(city)) = LOWER(TRIM(%s))
                """

                params.append(city)


            # =================================================
            # SPECIALIZATION
            # =================================================

            if specialization:

                from app.utils.specialist import (
                    get_specialization_keywords
                )

                keywords = get_specialization_keywords(
                    specialization
                )

                if keywords:

                    conditions = []

                    for keyword in keywords:

                        conditions.append(
                            "LOWER(specialization) LIKE %s"
                        )

                        params.append(
                            f"%{keyword.lower()}%"
                        )

                    sql += (
                        " AND ("
                        + " OR ".join(conditions)
                        + ")"
                    )

                else:

                    sql += """
                        AND LOWER(specialization) LIKE %s
                    """

                    params.append(
                        f"%{specialization.lower()}%"
                    )


            # =================================================
            # MINIMUM FEE
            # =================================================

            if min_fee is not None:

                sql += """
                    AND appointment_fee >= %s
                """

                params.append(min_fee)


            # =================================================
            # MAXIMUM FEE
            # =================================================

            if max_fee is not None:

                sql += """
                    AND appointment_fee <= %s
                """

                params.append(max_fee)


            # =================================================
            # AVAILABILITY
            # =================================================

            if availability is not None:

                availability_value = None

                if str(availability).lower() in [
                    "available",
                    "1",
                    "true"
                ]:
                    availability_value = 1

                elif str(availability).lower() in [
                    "unavailable",
                    "0",
                    "false"
                ]:
                    availability_value = 0

                if availability_value is not None:

                    sql += """
                        AND availability = %s
                    """

                    params.append(
                        availability_value
                    )


            # =================================================
            # ORDER
            # =================================================

            sql += """
                ORDER BY appointment_fee ASC
            """


            print("SQL:", sql)
            print("PARAMS:", params)

            cursor.execute(
                sql,
                tuple(params)
            )

            return cursor.fetchall()

    finally:

        connection.close()


# =========================================================
# GET DOCTORS BY SPECIALIZATION CATEGORY
# =========================================================

def get_doctors_by_specialization(
    specialization: str
):
    """
    Returns doctors matching a medical specialization
    category.

    The database contains detailed specialization names,
    so multiple keywords are used for matching.
    """

    from app.utils.specialist import (
        get_specialization_keywords
    )

    connection = get_connection()

    if connection is None:
        return []

    try:

        keywords = get_specialization_keywords(
            specialization
        )

        with connection.cursor() as cursor:

            # -------------------------------------------------
            # FALLBACK
            # -------------------------------------------------

            if not keywords:

                sql = """
                    SELECT *
                    FROM doctors
                    WHERE is_active = 1
                    AND LOWER(specialization) LIKE %s
                    ORDER BY appointment_fee ASC
                """

                cursor.execute(
                    sql,
                    (
                        f"%{specialization.lower()}%",
                    )
                )

                return cursor.fetchall()


            # -------------------------------------------------
            # KEYWORD MATCHING
            # -------------------------------------------------

            conditions = []

            params = []

            for keyword in keywords:

                conditions.append(
                    "LOWER(specialization) LIKE %s"
                )

                params.append(
                    f"%{keyword.lower()}%"
                )


            where_clause = " OR ".join(
                conditions
            )


            sql = f"""
                SELECT *
                FROM doctors
                WHERE is_active = 1
                AND ({where_clause})
                ORDER BY appointment_fee ASC
            """


            cursor.execute(
                sql,
                tuple(params)
            )


            return cursor.fetchall()

    finally:

        connection.close()


# =========================================================
# GET ALL SPECIALIZATIONS
# =========================================================

def get_all_specializations():
    """
    Returns all unique active specializations
    directly from the doctors table.
    """

    connection = get_connection()

    if connection is None:
        return []

    try:

        with connection.cursor() as cursor:

            sql = """
                SELECT DISTINCT specialization
                FROM doctors
                WHERE is_active = 1
                AND specialization IS NOT NULL
                AND specialization != ''
                ORDER BY specialization
            """

            cursor.execute(sql)

            return cursor.fetchall()

    finally:

        connection.close()


# =========================================================
# SEARCH SPECIALIZATIONS
# =========================================================

def search_specializations(
    name: str
):
    """
    Search unique specializations directly
    from the doctors table.
    """

    connection = get_connection()

    if connection is None:
        return []

    try:

        with connection.cursor() as cursor:

            sql = """
                SELECT DISTINCT specialization
                FROM doctors
                WHERE is_active = 1
                AND specialization IS NOT NULL
                AND specialization != ''
                AND specialization LIKE %s
                ORDER BY specialization
            """

            cursor.execute(
                sql,
                (
                    f"%{name}%",
                )
            )

            return cursor.fetchall()

    finally:

        connection.close()