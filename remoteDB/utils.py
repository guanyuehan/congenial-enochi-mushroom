import sqlite3 
import os 
def connect_db(path):
	try:
		conn = sqlite3.connect(path)
		return conn
	except sqlite3.Error as e:
		print(f"Error connecting to database: {e}")
		return None

def check_db_file_size(limit=100): # prevents spam
	'''
	checks if file size is within limit to prevent spam 

	Args: 
	limit (int): max file size in megabytes 

	Returns:
	(bool): True if file size is within limit, False otherwise
	'''
	file_size = os.path.getsize('database.db')
	file_size_mb = file_size / (1024 * 1024)
	return file_size_mb <= limit