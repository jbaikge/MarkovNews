from HTMLParser import HTMLParser

from BrainBase import BrainBase

class PageParser(HTMLParser):
	def __init__(self, url):
		self.brainbase = BrainBase()
		self.origin_id = self.brainbase.get_id("origin", url)
		HTMLParser.__init__(self)

	def handle_data(self, data):
		words = data.split()
		for word in words:
			print word,
			word_id = self.brainbase.get_id("word", word)
			self.brainbase.add_word_path(self.origin_id, word_id)
