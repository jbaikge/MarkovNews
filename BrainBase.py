import sqlite3

class BrainBase:
	def __init__(self, filename = './brainbase.db'):
		self.filename = filename
		self.connection = sqlite3.connect(self.filename)
		self.cursor = self.connection.cursor()
	def initialize(self):
		creates = [
			"""CREATE TABLE IF NOT EXISTS categories (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT,
				UNIQUE(name)
			)""",
			"""CREATE TABLE IF NOT EXISTS origins (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				url TEXT,
				added INTEGER,
				UNIQUE(url)
			)""",
			"""CREATE TABLE IF NOT EXISTS words (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				word TEXT NOT NULL,
				UNIQUE(word)
			)""",
			"""CREATE TABLE IF NOT EXISTS wordpaths (
				current_word INTEGER,
				next_word INTEGER NOT NULL,
				origin_id INTEGER NOT NULL,
				FOREIGN KEY current_word REFERENCES words(id) ON DELETE CASCADE,
				FOREIGN KEY next_word REFERENCES words(id) ON DELETE CASCADE,
				FOREIGN KEY origin_id REFERENCES origins(id) ON DELETE CASCADE
			)"""
		]
		for sql in creates:
			self.cursor.execute(sql)
		self.connection.commit()
		
		

bb = BrainBase()
bb.initialize()
