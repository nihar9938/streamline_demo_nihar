import pyodbc
import pandas as pd

# Database connection details
DB_HOST = "your_sybase_host"  # e.g., "192.168.1.100"
DB_PORT = "2638"  # Default port for Sybase IQ
DB_NAME = "your_database"
DB_USER = "your_username"
DB_PASSWORD = "your_password"

# ODBC Connection String (Using DSN)
# conn_str = "DSN=your_dsn_name;UID=your_username;PWD=your_password"

# ODBC Connection String (Without DSN)
conn_str = f"DRIVER={{Sybase IQ}};HOST={DB_HOST};PORT={DB_PORT};DBN={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD}"

try:
    # Connect to Sybase IQ
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Define the SQL query
    query = "SELECT * FROM your_table LIMIT 10"  # Adjust as needed
    
    # Read data into a Pandas DataFrame
    df = pd.read_sql(query, conn)
    
    # Print the result
    print(df)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()





from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(f"sybase+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=Sybase+IQ")

query = "SELECT * FROM your_table LIMIT 10"
df = pd.read_sql(query, engine)

print(df)


pip install pyodbc pandas
pip install sqlalchemy
