import sqlite3
import time

class BrainBase:
	def __init__(self):
		self.connect()
		self.create_tables()
	def connect(self):
		self.filename = './brainbase.sqlite'
		self.connection = sqlite3.connect(self.filename)
		self.cursor = self.connection.cursor()
	def create_tables(self):
		creates = [
			"""CREATE TABLE IF NOT EXISTS categories (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT UNIQUE
			)""",
			"""CREATE TABLE IF NOT EXISTS origins (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				url TEXT UNIQUE,
				added INTEGER
			)""",
			"""CREATE TABLE IF NOT EXISTS words (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				word TEXT NOT NULL UNIQUE
			)""",
			"""CREATE TABLE IF NOT EXISTS wordpaths (
				position INTEGER,
				current INTEGER REFERENCES words(id) ON DELETE CASCADE,
				next INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
				origin_id INTEGER NOT NULL REFERENCES origins(id) ON DELETE CASCADE
			)"""
		]
		for sql in creates:
			self.cursor.execute(sql)
		self.connection.commit()
	def get_id(self, object_type, definition):
		valid_types = {
			"category": {
				"table": "categories",
				"fields": ["name"]
			},
			"origin": {
				"table": "origins",
				"fields": ["url"],
				"inserts": 
			},
			"word": {
				"table": "words",
				"fields": ["word"]
			}
		}
		if object_type not in valid_types:
			raise KeyError
		valid_type = valid_types[object_type]
		definition_keys = definition.keys()
		fields = valid_type['fields']
		definition_keys.sort()
		fields.sort()
		if definition_keys != fields:
			print "Required attributes:", fields, "; fields given:", definition_keys
			raise AttributeError
		table_info = (valid_type['table'], valid_type['fields'][0])
		self.cursor.execute("SELECT id FROM %s WHERE %s = ?" % table_info, definition.values())
		row = self.cursor.fetchone()
		if row is None:
			self.cursor.execute("INSERT INTO %s (%s) VALUES (?)" % table_info, definition.values())
			id = self.cursor.lastrowid
			self.connection.commit()
		else:
			id = row[0]
		return id

class Category(BrainBase):
	def __init__(self, name):
		self.connect()
		self.name = name
		row = self.cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
		if row is None:
			self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
			self.id = self.cursor.lastrowid
			self.connection.commit()
		else:
			self.id = row[0]

class Origin(BrainBase):
	def __init__(self, url):
		self.connect()
		self.url = url
		row = self.cursor.execute("SELECT id FROM origins WHERE url = ?", (url,)).fetchone()
		if row is None:
			self.cursor.execute("INSERT OR IGNORE INTO origins (url, added) VALUES (?, ?)", (url, time.time()))
			self.id = self.cursor.lastrowid
			self.connection.commit()
		else:
			self.id = row[0]

class Word(BrainBase):
	def __init__(self, word):
		self.connect()
		self.cursor.execute("SELECT id FROM words WHERE word = ?", (word,))
		# self.cursor.rowcount returns -1 for all sqlite queries. Using
		# fetchone and checking for None instead.
		row = self.cursor.fetchone()
		if row is None:
			self.cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
			self.id = self.cursor.lastrowid
			self.connection.commit()
		else:
			self.id = row[0]

class WordPath(BrainBase):
	def __init__(self):
		self.connect()
		self.position = 0
		self.previous_word = Word('')
	def set_origin(self, origin):
		print type(origin)
		self.origin = origin
	def add_word(self, word):
		path = (self.position, self.previous_word.id, word.id, self.origin.id)
		self.cursor.execute("INSERT INTO wordpaths (position, current, next, origin_id) VALUES (?, ?, ?, ?)", path)
		self.position = self.position + 1
		self.previous_word = word
