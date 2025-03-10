import pyodbc

# Connection parameters
conn_str = (
    r'DRIVER={Adaptive Server Enterprise};'
    r'SERVER=your_server_address;'
    r'PORT=your_server_port;'
    r'DATABASE=your_database_name;'
    r'UID=your_username;'
    r'PWD=your_password;'
)

try:
    # Establish connection
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT * FROM your_table")

    # Fetch results
    rows = cursor.fetchall()

    # Print results
    for row in rows:
        print(row)

except pyodbc.Error as ex:
    print(f"Error connecting to Sybase ASE: {ex}")

finally:
    # Close connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
