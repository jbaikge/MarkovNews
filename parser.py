#!/usr/bin/env python
import feedparser
from HTMLParser import HTMLParser
import sqlite3
import urllib2

class PageParser(HTMLParser):
	ignore_tags = ['script', 'title', 'style']
	allow_tags = ['p']

	def __init__(self):
		self.words = []
		self.collect_data = True
		HTMLParser.__init__(self)

	def handle_data(self, data):
		if self.collect_data:
			self.words.extend(data.split())

	def handle_endtag(self, tag):
		if self.collect_data and tag in self.allow_tags:
			self.words += ['']

	def handle_starttag(self, tag, attrs):
		self.collect_data = tag not in self.ignore_tags
		self.collect_data = self.collect_data or tag in self.allow_tags
		self.collect_data = self.collect_data and len(attrs) == 0

def create_tables(connection):
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
		"""INSERT OR IGNORE INTO words (id, word) VALUES (1, '')""",
		"""CREATE TABLE IF NOT EXISTS wordpaths (
			position INTEGER,
			word1 INTEGER REFERENCES words(id) ON DELETE CASCADE,
			word2 INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
			origin_id INTEGER NOT NULL REFERENCES origins(id) ON DELETE CASCADE,
			UNIQUE(position, origin_id)
		)"""
	]
	for sql in creates:
		connection.execute(sql)

def add_word_path(connection, position, origin_id, word_ids):
	word1, word2 = word_ids
	args = (position, word1, word2, origin_id)
	connection.execute("""INSERT OR IGNORE INTO wordpaths 
		(position, word1, word2, origin_id)
		VALUES (?, ?, ?, ?)""", args)

def add_words(connection, url, words):
	origin_id = get_origin_id(connection, url)
	word1 = words[0]
	word_id_cache = {
		word1: get_word_id(connection, word1)
	}
	position = 0
	for word2 in words[1:]:
		if word2 not in word_id_cache:
			word_id_cache[word2] = get_word_id(connection, word2)
		add_word_path(connection, position, origin_id, (word_id_cache[word1], word_id_cache[word2]))
		word1 = word2
		position += 1
	return True

def database_commit(connection):
	connection.commit()

def database_connect():
	return sqlite3.connect('brainbase.sqlite')

def feed_links(url):
	links = []
	feed = feedparser.parse(url)
	for entry in feed.entries:
		links.append(entry.link)
	return links

def get_origin_id(connection, url):
	connection.execute("INSERT OR IGNORE INTO origins (url) VALUES (?)", (url,))
	result = connection.execute("SELECT id FROM origins WHERE url = ?", (url,))
	return result.fetchone()[0]

def get_word_id(connection, word):
	connection.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word,))
	result = connection.execute("SELECT id FROM words WHERE word = ?", (word,))
	return result.fetchone()[0]

def get_words_from_url(url):
	contents = urllib2.urlopen(url).read().decode('utf-8')
	parser = PageParser()
	parser.feed(contents)
	return parser.words + ['']

def has_origin(connection, url):
	result = connection.execute("SELECT id FROM origins WHERE url = ?", (url,))
	return result.fetchone() != None

def rss_urls():
	return [
		"http://www.theregister.co.uk/headlines.atom",
	]

if __name__ == "__main__":
	print "Connect"
	connection = database_connect()
	print "Auto-Create Tables"
	create_tables(connection)
	print "Process RSS Feeds"
	for rss in rss_urls():
		print " RSS: %s" % (rss,)
		for link in feed_links(rss):
			print " ", link.split('/')[-2],
			if has_origin(connection, link):
				print "Stored"
			else:
				words = get_words_from_url(link)
				if add_words(connection, link, words):
					database_commit(connection)
				print len(words)
