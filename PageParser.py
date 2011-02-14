from HTMLParser import HTMLParser

from BrainBase import WordPath, Word

class PageParser(HTMLParser):

	def set_origin(self, origin):
		self.path = WordPath()
		self.path.set_origin(origin)

	def handle_data(self, data):
		words = data.split()
		for word in words:
			self.path.add_word(Word(word))
