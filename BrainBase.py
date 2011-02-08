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
				current INTEGER,
				next INTEGER NOT NULL,
				origin_id INTEGER NOT NULL,
				FOREIGN KEY (current) REFERENCES words(id) ON DELETE CASCADE,
				FOREIGN KEY (next) REFERENCES words(id) ON DELETE CASCADE,
				FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE
			)"""
		]
		for sql in creates:
			self.cursor.execute(sql)
		self.connection.commit()
	def category(self, category_name):
		self.cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
		self.connection.commit()
		self.cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
		return self.cursor.fetchone()[0]
	def origin(self, url):
		self.cursor.execute("INSERT OR IGNORE INTO origins (url, added) VALUES (?, ?)", (url, time.time()))
		self.connection.commit()
		self.cursor.execute("SELECT id FROM origins WHERE url = ?", (url,))
		return self.cursor.fetchone()[0]

bb = BrainBase()
bb.initialize()
print "Category 'Tech': %d" % bb.category('Tech')
print "Category 'IT': %d" % bb.category('IT')
print "URL 'http://www.google.com': %d" % bb.origin('http://www.google.com')
print "URL 'http://www.monkeys.com': %d" % bb.origin('http://www.monkey.com')
