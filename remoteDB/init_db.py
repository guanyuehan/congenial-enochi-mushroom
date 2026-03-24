import sqlite3
import os

def connect_db(path):
	try:
		conn = sqlite3.connect(path)
		conn.row_factory = sqlite3.Row
		return conn
	except sqlite3.Error as e:
		print(f"Error connecting to database: {e}")
		return None

def init_database(db_path='database.db'):
	conn = connect_db(db_path)
	
	if conn is None:
		return False
	
	# Create tables if they don't exist
	conn.execute('''
	CREATE TABLE IF NOT EXISTS "posts" (
		"id"	TEXT PRIMARY KEY,
		"content"	TEXT NOT NULL,
		"date"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	''')
	
	conn.commit()
	conn.close()
	
	print(f"Database initialized at {db_path}")
	return True

if __name__ == "__main__":
	init_database()