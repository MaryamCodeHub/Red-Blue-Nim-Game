import sqlite3

def inspect_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(table[0])

    # Show schema for each table
    for table_name in [table[0] for table in tables]:
        print(f"\nSchema for table '{table_name}':")
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()
        for column in schema:
            print(column)

    conn.close()

# Provide the path to your database
inspect_database(r"C:\Users\DELL\source\repos\PythonApplication4\PythonApplication4\instance\database.db")
