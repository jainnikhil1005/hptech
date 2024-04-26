import sqlite3

def list_tables_and_schema(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Print all tables and their schema
    for table_name in tables:
        print(f"Table: {table_name[0]}")
        cursor.execute(f"PRAGMA table_info({table_name[0]})")
        columns = cursor.fetchall()
        for column in columns:
            print(column)

    # Close the connection to the database
    conn.close()

# Usage
db_path = '/Users/nikhiljain/Nikhil/TAMU/Freshman Year/HpTech/rosbag2_2024_03_20-18_12_58_0.db3'
list_tables_and_schema(db_path)
