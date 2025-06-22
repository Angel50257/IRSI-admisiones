import urllib.parse

class Config:
    DB_SERVER = 'DESKTOP-M9L8G75'  # Nota la coma y el puerto explícito
    DB_NAME = 'Admisiones'
    DB_USER = 'coder'
    DB_PASSWORD = 'coder'

    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )

    params = urllib.parse.quote_plus(connection_string)
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clave-backup-solo-desarrollo'
