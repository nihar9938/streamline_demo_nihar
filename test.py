import pyodbc

# Define connection parameters
conn_str = (
    "DRIVER={Adaptive Server Enterprise};"
    "SERVER=your_server;"
    "PORT=5000;"
    "DATABASE=your_db;"
    "UID=your_username;"
    "PWD=your_password"
)

# Establish connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Execute a query
query = "SELECT * FROM your_table"
cursor.execute(query)

# Fetch results
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

# Close connection
cursor.close()
conn.close()
