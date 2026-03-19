from flask import Flask, request, jsonify
from utils import connect_db, check_db_file_size
import sqlite3

app = Flask(__name__) 

@app.route('/api/get_posts', methods=['POST'])
def request_table_data():
	'''
	requests data from a specified table in the database

	Post parameters (json):
	table_name (str): name of the table to request data from

	Returns:
	(list of dicts): list of dictionaries, each representing a row in the table
	'''
	# checks 
	if not check_db_file_size():
		return jsonify({'error': 'database file size exceeds limit'}), 400
	data = request.json
	post_id = data.get('post_id')
	user_id = data.get('user_id')
	if not post_id:
		return jsonify({'error': 'post_id is required'}), 400
	
	conn = connect_db('database.db')

	if not conn:
		return jsonify({'error': 'database connection failed'}), 500
	try:
		cursor = conn.cursor()
		cursor.execute(f"SELECT * FROM {table_name}")
		rows = cursor.fetchall()
		conn.close()
		return jsonify(rows), 200, {'Content-Type': 'application/json'}
	except sqlite3.Error as e:
		print(f"Error querying database: {e}")
		return jsonify({'error': 'database query failed'}), 500
		
