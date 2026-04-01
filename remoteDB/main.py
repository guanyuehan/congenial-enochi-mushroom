from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import uuid
from datetime import datetime
from init_db import init_database, connect_db

app = Flask(__name__)
CORS(app)

DB_PATH = 'database.db'

# Initialize database on startup
init_database(DB_PATH)

def get_db():
	conn = connect_db(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn

@app.route('/api/posts', methods=['GET'])
def get_posts():
	"""Get all posts ordered by date (newest first)"""
	try:
		conn = get_db()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM posts ORDER BY date DESC')
		rows = cursor.fetchall()
		posts = [dict(row) for row in rows]
		conn.close()
		return jsonify(posts), 200
	except Exception as e:
		print(f"Error getting posts: {e}")
		return jsonify({"error": str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def create_post():
	"""Create a new post"""
	try:
		data = request.json
		
		if not data.get('content'):
			return jsonify({"error": "Content is required"}), 400
		
		conn = get_db()
		cursor = conn.cursor()
		
		post_id = str(uuid.uuid4())
		cursor.execute('''
			INSERT INTO posts (id, content, date)
			VALUES (?, ?, ?)
		''', (post_id, data['content'], datetime.now().isoformat()))
		
		conn.commit()
		conn.close()
		
		return jsonify({
			"id": post_id,
			"content": data['content'],
			"date": datetime.now().isoformat()
		}), 201
	except Exception as e:
		print(f"Error creating post: {e}")
		return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
	"""Get a single post by ID"""
	try:
		conn = get_db()
		cursor = conn.cursor()
		cursor.execute('SELECT content, date FROM posts WHERE id = ?', (post_id,))
		row = cursor.fetchone()
		conn.close()
		
		if not row:
			return jsonify({"error": "Post not found"}), 404
		
		return jsonify(dict(row)), 200
	except Exception as e:
		print(f"Error getting post: {e}")
		return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
	"""Delete a post by ID"""
	try:
		conn = get_db()
		cursor = conn.cursor()
		cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
		conn.commit()
		conn.close()
		return jsonify({"message": "Post deleted"}), 200
	except Exception as e:
		print(f"Error deleting post: {e}")
		return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
	"""Health check endpoint"""
	return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
	print("Starting Remote DB Server on http://localhost:5000")
	app.run(host='localhost', port=5000, debug=False)