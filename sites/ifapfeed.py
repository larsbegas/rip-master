#!/usr/bin/python

import sys 

from Httpy import Httpy
from Web import Web
import mechanize, re, time, calendar
from datetime import datetime, timedelta
from site_imagefap    import imagefap
from pymongo import MongoClient

for gall in sys.argv[1:]:
	print gall
	

#whynot 494927
#jimmy 1764181
asd = 'http://www.imagefap.com/ajax/newsdata.php?userid=1764181&status=&galleries=&comments=&ts='


mongo = MongoClient()

rGall = re.compile('href="\/gallery\/(\d+)"><b>[^<]+<\/b>')
web = Web()

ts = datetime.now()
ts2 = ts - timedelta(days=5)
sss = calendar.timegm(ts2.utctimetuple())
print sss
#exit()
ar = set()
feed = web.get('http://www.imagefap.com/newsfeed.php?user=JimmyPerv77')
for a in re.findall(rGall, feed):
	a2 = 'http://www.imagefap.com/gallery/' + str(a)
	print a2
	if mongo.feed.url.find_one({"url": a2}):
		print "1found %s" % a2
		continue
	ar.add(a2)
	#mongo.feed.url.insert({"url":  str(a2)})
	#i = imagefap(a2, debugging=True)
	#i.download()
	

for i in range(1,2):
	print i
	ts3 = ts - timedelta(days=i)
	sss3 = calendar.timegm(ts3.utctimetuple())
	feed3 = web.get(asd + str(sss3))
	for c in re.findall(rGall, feed3):
		ar.add(c)
	
for gg in ar:
	gg2 = 'http://imagefap.com/gallery/' + str(gg)
	if mongo.feed.url.find_one({"url": str(gg2)}):
		print "found %s" % gg2
		continue
	else:
		i = imagefap(gg2, debugging=True)
		i.download()
		mongo.feed.url.insert({"url":  str(gg2)})
	
exit(ar)

feed2 = web.get(asd+ str(sss))
for b in re.findall(rGall, feed2):
	print b	