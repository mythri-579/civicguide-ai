import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

POSTGRES_PASSWORD = "Mythri"

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password='Mythri',
    host="localhost",
    port="5432"
)

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor()

cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'civicguide_db'")
exists = cursor.fetchone()

if exists:
    print("Database civicguide_db already exists")
else:
    cursor.execute("CREATE DATABASE civicguide_db")
    print("Database civicguide_db created successfully")

cursor.close()
connection.close()