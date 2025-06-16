import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-M9L8G75;"
    "DATABASE=Admisiones;"
    "UID=coder;"
    "PWD=123456;"
)

class Config:
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clave-super-secreta'