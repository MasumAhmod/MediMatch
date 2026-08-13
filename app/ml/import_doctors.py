import os
import pandas as pd
import pymysql
from dotenv import load_dotenv


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

MYSQLHOST = os.environ["MYSQLHOST"]
MYSQLPORT = os.environ["MYSQLPORT"]
MYSQLUSER = os.environ["MYSQLUSER"]
MYSQLPASSWORD = os.environ["MYSQLPASSWORD"]
MYSQLDATABASE = os.environ["MYSQLDATABASE"]
MYSQL_SSL_CA = os.environ["MYSQL_SSL_CA"]


# ============================================================
# Load CSV
# ============================================================

csv_path = "app/ml/datasets/doctorData.csv"

df = pd.read_csv(csv_path)

# Remove unwanted CSV index column
df = df.drop(columns=["Unnamed: 10"], errors="ignore")

print("CSV rows:", len(df))
print("CSV columns:", df.columns.tolist())


# ============================================================
# Connect to Aiven MySQL
# ============================================================

print("Connecting to Aiven MySQL...")

connection = pymysql.connect(
    host=MYSQLHOST,
    port=int(MYSQLPORT),
    user=MYSQLUSER,
    password=MYSQLPASSWORD,
    database=MYSQLDATABASE,
    ssl={
        "ca": MYSQL_SSL_CA
    }
)

print("Successfully connected to Aiven MySQL.")


# ============================================================
# Insert doctors
# ============================================================

cursor = connection.cursor()

sql = """
INSERT INTO doctors (
    doctor_name,
    degree,
    specialization,
    designation,
    current_workplace,
    chamber_hospital,
    city,
    visiting_hours,
    appointment_phone,
    appointment_fee
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
"""


count = 0

for _, row in df.iterrows():

    cursor.execute(
        sql,
        (
            row["doctor_name"],
            row["degree"],
            row["specialization"],
            row["designation"],
            row["current_workplace"],
            row["chamber_hospital"],
            row["city"],
            row["Visiting_Hour"],
            row["Appointment_Phone"],
            row["Appointment_Fee"]
        )
    )

    count += 1


# ============================================================
# Save changes
# ============================================================

connection.commit()

print(f"Successfully inserted {count} doctors.")


# ============================================================
# Close connection
# ============================================================

cursor.close()
connection.close()

print("Database connection closed.")