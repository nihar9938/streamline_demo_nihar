from sqlalchemy import create_engine
import urllib
import pandas as pd

DB_HOST = "your_sybase_host" 
DB_PORT = "5000"              
DB_NAME = "your_database"
DB_USER = "your_username"
DB_PASSWORD = "your_password"

odbc_str = f"DRIVER={{Sybase ASE ODBC Driver}};SERVER={DB_HOST};PORT={DB_PORT};DB={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"
odbc_str_encoded = urllib.parse.quote_plus(odbc_str)  

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={odbc_str_encoded}")

query = "SELECT TOP 10 * FROM your_table"  

df = pd.read_sql(query, engine)

print(df)
