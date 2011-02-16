import feedparser
import urllib2

import BrainBase
from PageParser import PageParser

urls = [
	#"file:///usr/share/doc/python-doc/html/library/sys.html",
	#"file:///usr/share/doc/python-doc/html/library/warnings.html",
	#"file:///usr/share/doc/python-doc/html/library/urllib2.html"
]
for url in urls:
	p = PageParser(url)
	p.feed(urllib2.urlopen(url).read())
	p.save()

feed_urls = [
	"http://www.theregister.co.uk/headlines.atom",
	#"/home/jake/git/MarkovNews/headlines.atom",
	"http://feeds.foxnews.com/foxnews/national?format=xml",
	"http://feeds.foxnews.com/foxnews/scitech?format=xml",
]

for feed_url in feed_urls:
	feed = feedparser.parse(feed_url)
	for entry in feed.entries:
		print entry.link,
		PageParser(entry.link)

#SELECT current_word.word, next_word.word, count(*) AS cnt FROM wordpaths LEFT JOIN words AS current_word ON(current = current_word.id) LEFT JOIN words AS next_word ON(next = next_word.id) GROUP BY current, next ORDER BY cnt DESC LIMIT 30;
