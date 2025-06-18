import urllib.parse
import os

class Config:
    # Configuración de la base de datos
    DB_SERVER = os.environ.get('DB_SERVER', 'localhost\\SQLEXPRESS')  # Asegurar formato SERVIDOR\\INSTANCIA
    DB_NAME = os.environ.get('DB_NAME', 'Admisiones')
    DB_USER = os.environ.get('DB_USER', '')  # Para autenticación SQL
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')  # Para autenticación SQL
    
    # Cadena de conexión dinámica
    if DB_USER and DB_PASSWORD:
        # Autenticación con usuario y contraseña
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD}"
        )
    else:
        # Autenticación Windows (Trusted Connection)
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
    
    # Codificación para URL
    params = urllib.parse.quote_plus(connection_string)
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-backup-solo-desarrollo')