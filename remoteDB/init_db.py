import sqlite3

def connect_db(path):
	try:
		conn = sqlite3.connect(path)
		return conn
	except sqlite3.Error as e:
		print(f"Error connecting to database: {e}")
		return None
	
'''
schema 
CREATE TABLE "users" (
	"id"	TEXT,
	"username"	VARCHAR(255),
	"profile_picture"	BLOB,
	PRIMARY KEY("id","username")
);



CREATE TABLE "posts" (
	"user"	TEXT,
	"content"	TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL CHECK("timestamp" LIKE '____-__-__ __:__'),
	 FOREIGN KEY("user") REFERENCES "users"("username")
);
'''

conn = connect_db('database.db')
conn.execute('''
CREATE TABLE "users" (
	"id"	TEXT,
	"username"	VARCHAR(255) UNIQUE,
	"password"	VARCHAR(255),
	PRIMARY KEY("id")
);
''')

conn.execute('''
CREATE TABLE "posts" (
	"id"	TEXT,
	"username"	TEXT,
	"title"	TEXT,
	"content"	TEXT NOT NULL,
	PRIMARY KEY("id")
	FOREIGN KEY("username") REFERENCES "users"("username")
''') 

# conn.execute('''
# CREATE TABLE profile_pictures (
# 	"username"	TEXT,
# 	"profile_picture"	BLOB,
# 	PRIMARY KEY("username")
# 	FOREIGN KEY("username") REFERENCES "users"("username")
# );
# ''')


