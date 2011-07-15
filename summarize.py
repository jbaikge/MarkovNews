#!/usr/bin/env python
import sqlite3

def database_connect():
	return sqlite3.connect('brainbase.sqlite')

if __name__ == "__main__":
	print "Connect"
	connection = database_connect()

	print "Determining seed word"
	result = connection.execute("SELECT id FROM words ORDER BY RANDOM() LIMIT 1")
	seed_id = result.fetchone()[0]
	print "Seed ID:", seed_id

	query = """SELECT b.word2, a.word1, b.word1, w1.word, w2.word
		FROM wordpaths a
			LEFT JOIN wordpaths b ON(a.word2 = b.word1 AND a.position + 1 = b.position AND a.origin_id = b.origin_id)
			LEFT JOIN words w1 ON(a.word1 = w1.id)
			LEFT JOIN words w2 ON(b.word1 = w2.id)
		WHERE a.word1 = ?
		ORDER BY RANDOM()
		LIMIT 1"""
	
	words = []
	id = seed_id
	for _ in range(1, 100):
		result = connection.execute(query, (id,))
		row = result.fetchone()

		# Not sure what causes this yet
		if row[0] == None:
			break
		id = row[0]

		kill_loop = False
		for word in row[3:]:
			if word == '':
				kill_loop = True
				break
			else:
				words += [word]
		
		if kill_loop:
			break
	
	print ' '.join(words)