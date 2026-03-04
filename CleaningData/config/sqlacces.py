from dotenv import load_dotenv
import os
import pyodbc
from urllib.parse import quote_plus
import platform

load_dotenv()
# --------------------------------------------------------------------------------------
# Connection parameters for .17 
server = os.environ['DB_NAME_SERVER']  # e.g., 'localhost' or '192.168.1.100'
database = os.environ['DB_DATABASE']    # Name of your database
username = os.environ['DB_USER']
password = os.environ['DB_PASSWORD']
password = quote_plus(password)
sistema = platform.system()
if sistema == "Windows":
        driver = f'{pyodbc.drivers()[3]}'  # Ensure the correct driver is installed
elif sistema == "Linux":
    driver = f'{pyodbc.drivers()[0]}'   # Ensure the correct driver is installed
connection_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}&TrustServerCertificate=yes"

connection_str_dw_fz = connection_str
