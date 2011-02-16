import sqlite3
import time

class BrainBase:
	types = {
		"category": ("categories", "name"),
		"origin": ("origins", "url"),
		"word": ("words", "word")
	}

	def __init__(self):
		self.connect()
		self.create_tables()
		self.word_paths = {}

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
				added DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
			)""",
			"""CREATE TABLE IF NOT EXISTS words (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				word TEXT NOT NULL UNIQUE
			)""",
			"""CREATE TABLE IF NOT EXISTS wordpaths (
				position INTEGER,
				current INTEGER REFERENCES words(id) ON DELETE CASCADE,
				next INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
				origin_id INTEGER NOT NULL REFERENCES origins(id) ON DELETE CASCADE,
				UNIQUE(position, origin_id)
			)"""
		]
		for sql in creates:
			self.cursor.execute(sql)
		self.connection.commit()

	def exists(self, object_type, value):
		if object_type not in self.types:
			raise KeyError
		table_info = self.types[object_type]
		self.cursor.execute("SELECT id FROM %s WHERE %s = ?" % table_info, (value,))
		row = self.cursor.fetchone()
		if row is None:
			id = 0
		else:
			id = row[0]
		return id

	def get_id(self, object_type, value):
		id = self.exists(object_type, value)
		if id == 0:
			self.cursor.execute("INSERT INTO %s (%s) VALUES (?)" % self.types[object_type], (value,))
			id = self.cursor.lastrowid
		return id

	def save(self):
		self.connection.commit()

	def add_word_path(self, origin_id, word_id):
		if origin_id not in self.word_paths:
			self.word_paths[origin_id] = (self.get_id("word", ""), 0)
		(previous_word_id, position) = self.word_paths[origin_id]
		path = (position, previous_word_id, word_id, origin_id)
		self.cursor.execute("INSERT OR IGNORE INTO wordpaths (position, current, next, origin_id) VALUES (?, ?, ?, ?)", path)
		self.word_paths[origin_id] = (word_id, position + 1)

