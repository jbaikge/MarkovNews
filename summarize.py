#!/usr/bin/env python
import sqlite3

def database_connect():
	return sqlite3.connect('brainbase.sqlite')

if __name__ == "__main__":
	print "Connect"
	connection = database_connect()

	print "Determining seed word"
	result = connection.execute("""SELECT word1, word2
		FROM wordpaths
		WHERE word1 > 1 AND word2 > 1
		ORDER BY RANDOM()
		LIMIT 1""")
	word1_id, word2_id = result.fetchone()
	print "Seed IDs:", word1_id, word2_id

	query = """SELECT paths_b.word1, paths_b.word2, words_b.word
		FROM wordpaths paths_a
			LEFT JOIN wordpaths paths_b ON(
				paths_a.word2 = paths_b.word1
				AND paths_a.position + 1 = paths_b.position
				AND paths_a.origin_id = paths_b.origin_id
			)
			LEFT JOIN words words_b ON(paths_b.word1 = words_b.id)
		WHERE paths_a.word1 = ?
			AND paths_a.word2 = ?
		ORDER BY RANDOM()
		LIMIT 1"""
	
	words = []
	for _ in range(1, 100):
		result = connection.execute(query, (word1_id, word2_id))
		row = result.fetchone()
		if row == None or row[0] == None:
			break
		print row
		word1_id, word2_id, word = row
		if word == '':
			break;
		words.append(word)
	
	print ' '.join(words)