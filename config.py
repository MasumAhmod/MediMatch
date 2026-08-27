import os

from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_HOST = os.environ["MYSQLHOST"]
DB_PORT = int(os.environ["MYSQLPORT"])
DB_USER = os.environ["MYSQLUSER"]
DB_PASSWORD = os.environ["MYSQLPASSWORD"]
DB_NAME = os.environ["MYSQLDATABASE"]

print("===== DATABASE CONFIG =====")
print("DB_HOST:", DB_HOST)
print("DB_PORT:", DB_PORT)
print("DB_USER:", DB_USER)
print("DB_NAME:", DB_NAME)
print("===========================")


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

APP_NAME = "MediMatch"

APP_VERSION = "1.0.0"

DEBUG = True