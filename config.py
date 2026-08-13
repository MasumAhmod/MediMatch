import os


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_HOST = os.getenv(
    "MYSQLHOST",
    "localhost"
)

DB_PORT = int(
    os.getenv(
        "MYSQLPORT",
        "3306"
    )
)

DB_USER = os.getenv(
    "MYSQLUSER",
    "root"
)

DB_PASSWORD = os.getenv(
    "MYSQLPASSWORD",
    ""
)

DB_NAME = os.getenv(
    "MYSQLDATABASE",
    "medimatch"
)


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

APP_NAME = "MediMatch"

APP_VERSION = "1.0.0"

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"