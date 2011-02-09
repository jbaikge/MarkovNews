import sqlite3
import time

class BrainBase:
	def __init__(self, filename = './brainbase.db'):
		self.filename = filename
		self.connection = sqlite3.connect(self.filename)
		self.cursor = self.connection.cursor()
	def initialize(self):
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
	def category(self, category_name):
		self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
		self.cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
		self.connection.commit()
		return self.cursor.fetchone()[0]
	def origin(self, url):
		self.cursor.execute("INSERT OR IGNORE INTO origins (url, added) VALUES (?, ?)", (url, time.time()))
		self.cursor.execute("SELECT id FROM origins WHERE url = ?", (url,))
		self.connection.commit()
		return self.cursor.fetchone()[0]
	def word(self, word):
		self.cursor.execute("SELECT id FROM words WHERE word = ?", (word,))
		# self.cursor.rowcount returns -1 for all sqlite queries. Using
		# fetchone and checking for None instead.
		word_row = self.cursor.fetchone()
		if word_row is None:
			self.cursor.execute("INSERT INTO words (word) VALUES (?)", (word,))
			word_id = self.cursor.lastrowid
			self.connection.commit()
		else:
			word_id = word_row[0]
		return word_id
	def add_path(self, origin, position, current_word, next_word):
		self.cursor.execute("INSERT INTO wordpaths (position, current, next, origin_id) VALUES (?, ?, ?, ?)", (position, current_word, next_word, origin))
