from HTMLParser import HTMLParser
import urllib2

from BrainBase import BrainBase

class PageParser(HTMLParser):
	collect_data = True
	ignore_tags = ['script', 'title', 'style']

	def __init__(self, url):
		self.brainbase = BrainBase()
		if self.brainbase.exists("origin", url) == 0:
			print "parsing",
			self.origin_id = self.brainbase.get_id("origin", url)
			HTMLParser.__init__(self)

			contents = urllib2.urlopen(url).read().decode('utf-8')
			self.feed(contents)
			self.brainbase.save()
		print

	def handle_data(self, data):
		if not self.collect_data:
			return
		words = data.split()
		for word in words:
			try:
				word = word.decode('utf-8')
				word_id = self.brainbase.get_id("word", word)
				self.brainbase.add_word_path(self.origin_id, word_id)
			except UnicodeEncodeError:
				pass

	def handle_starttag(self, tag, attrs):
		self.collect_data = tag not in self.ignore_tags
