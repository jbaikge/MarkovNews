from HTMLParser import HTMLParser

import BrainBase

class PageParser(HTMLParser):

	def __init__(self, origin):
		self.origin = origin

	def handle_data(self, data):
		words = data.split(' ')
		for word in words:
			self.path.add_path()
