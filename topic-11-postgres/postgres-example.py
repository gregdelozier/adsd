import psycopg2

connection = None

try: 
    connection = psycopg2.connect(
        user = "example",
        password = "example",
        host = "localhost",
        port = "5432",
        database = "exampledb"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Version = ",record)

except Exception as e:
    print(f"Problem: {e}")

finally:
    if connection:
        cursor.close()
        connection.close()