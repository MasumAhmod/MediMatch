import os
from dotenv import load_dotenv


# Load .env when running locally.
# On Render, environment variables are provided by Render.
load_dotenv()


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_HOST = os.environ["MYSQLHOST"]

DB_PORT = int(
    os.environ["MYSQLPORT"]
)

DB_USER = os.environ["MYSQLUSER"]

DB_PASSWORD = os.environ["MYSQLPASSWORD"]

DB_NAME = os.environ["MYSQLDATABASE"]


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

APP_NAME = "MediMatch"

APP_VERSION = "1.0.0"

DEBUG = True