import psycopg2

# Define database connection parameters
db_config = {
    "dbname": "sampledb",
    "user": "user",
    "password": "",
    "host": "postgresql.my-data-science-project.svc.cluster.local",
    "port": "5432",  # Default is '5432'
}

try:
    # Establish the connection
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Example query
    query = "SELECT version();"

    # Execute the query
    cursor.execute(query)
    result = cursor.fetchone()

    print("PostgreSQL version:", result)

except psycopg2.Error as e:
    print(f"Error while connecting to PostgreSQL: {e}")
finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
        print("PostgreSQL connection closed.")
