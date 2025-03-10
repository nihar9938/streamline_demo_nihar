import pyodbc

# Define connection parameters
conn_str = "DRIVER={Adaptive Server Enterprise};SERVER=your_server;PORT=5000;DATABASE=your_db;UID=username;PWD=password"

# Establish connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM your_table")
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

# Close connection
cursor.close()
conn.close()
