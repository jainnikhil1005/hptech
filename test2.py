import sqlite3

def extract_sample_data(db_file_path, topic_name):
    print("Connecting to database...")
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    query = f"""
    SELECT data 
    FROM messages m
    JOIN topics t ON m.topic_id = t.id
    WHERE t.name = '{topic_name}'
    LIMIT 10
    """
    print("Executing query...")
    cursor.execute(query)
    samples = cursor.fetchall()
    print("Data fetched successfully.")
    conn.close()
    return samples

# Usage
db_path = '/Users/nikhiljain/Nikhil/TAMU/Freshman Year/HpTech/rosbag2_2024_03_20-18_12_58_0.db3'
topic_name = '/rel_angle'
print(f"Fetching samples for topic: {topic_name}")
samples = extract_sample_data(db_path, topic_name)
print("Samples:")
print(samples)
