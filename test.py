import urllib2

import BrainBase
from PageParser import PageParser

#url = 'http://www.theregister.co.uk/2011/02/11/nokia_microsoft_more_details/'

#o = BrainBase.Origin(url)
#f = urllib2.urlopen(url)
#p = PageParser()
#p.set_origin(o)
#content = f.read()
#p.feed(content)

urls = [
	"file:///usr/share/doc/python-doc/html/library/sys.html",
	"file:///usr/share/doc/python-doc/html/library/warnings.html",
	"file:///usr/share/doc/python-doc/html/library/urllib2.html"
]
for url in urls:
	p = PageParser(url)
	p.feed(urllib2.urlopen(url).read())

#db = BrainBase.BrainBase()
#print db.get_id("category", {"name": "Technology"})
#print db.get_id("word", {"word": "oink"})
#print db.get_id("origin", {"url": "http://www.google.com"})
