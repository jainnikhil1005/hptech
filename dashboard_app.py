from flask import Flask, render_template, jsonify
import sqlite3
import pandas as pd
import numpy as np
import json
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

def fetch_data_from_db(db_file_path, query):
    # Connect to the SQLite database and execute a query
    with sqlite3.connect(db_file_path) as conn:
        return pd.read_sql_query(query, conn)

def decode_binary_data(binary_data):
    if binary_data:
        print(f"Data length: {len(binary_data)}")
        if len(binary_data) >= 8:  # Ensure there's at least one float64 worth of data
            float_data = np.frombuffer(binary_data[:8], dtype=np.float64)[0]
            extra_data = binary_data[8:]  # Capture the remaining bytes
            print(f"Extra data: {extra_data.hex()}")  # Log extra data as hex for analysis
            return float_data
        else:
            print("Data length is not suitable for float64 decoding.")
    return None


def read_and_process_data(db_file_path, topic_name):
    conn = sqlite3.connect(db_file_path)
    query = f"""
    SELECT timestamp, data
    FROM messages m
    JOIN topics t ON m.topic_id = t.id
    WHERE t.name = '{topic_name}'
    """
    cursor = conn.cursor()
    cursor.execute(query)
    raw_samples = cursor.fetchall()
    conn.close()
    
    processed_samples = []
    for timestamp, data in raw_samples:
        decoded_data = decode_binary_data(data)
        if decoded_data is not None:
            processed_samples.append((timestamp, decoded_data))
        else:
            print(f"Failed to decode data: {data}")
    return processed_samples


def create_line_chart(data, title):
    df = pd.DataFrame(data, columns=['timestamp', 'value'])
    fig = px.line(df, x='timestamp', y='value', title=title)
    return json.dumps(fig, cls=PlotlyJSONEncoder)

@app.route('/')
def dashboard():
    db_path = '/Users/nikhiljain/Nikhil/TAMU/Freshman Year/HpTech/rosbag2_2024_03_20-18_12_58_0.db3'
    data = read_and_process_data(db_path, '/steering_angle')  # Example to fetch and decode steering angle data
    line_chart = create_line_chart(data, 'Dashboard Overview')
    return render_template('dashboard.html', line_chart=json.dumps(line_chart))

@app.route('/steering_angle')
def steering_angle_data():
    db_file_path = '/Users/nikhiljain/Nikhil/TAMU/Freshman Year/HpTech/rosbag2_2024_03_20-18_12_58_0.db3'
    data = read_and_process_data(db_file_path, '/steering_angle')
    chart_data = create_line_chart(data, 'Steering Angle Over Time')
    return jsonify(chart_data)

@app.route('/rel_angle')
def rel_angle_data():
    db_file_path = '/Users/nikhiljain/Nikhil/TAMU/Freshman Year/HpTech/rosbag2_2024_03_20-18_12_58_0.db3'
    data = read_and_process_data(db_file_path, '/rel_angle')
    chart_data = create_line_chart(data, 'Relative Angle Over Time')
    return jsonify(chart_data)

@app.route('/fv_vel')
def fv_vel_data():
    db_file_path = '/Users/nikhiljain/Nikhil/TAMU/Freshman Year/HpTech/rosbag2_2024_03_20-18_12_58_0.db3'
    data = read_and_process_data(db_file_path, '/FV_vel')
    chart_data = create_line_chart(data, 'Vehicle Speed Over Time')
    return jsonify(chart_data)
if __name__ == '__main__':
    app.run(debug=True)
