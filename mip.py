#!/usr/bin/python

from sys import exit
import sys

for gall in sys.argv[1:]:
	try:
		print gall	
		pass
	except Exception, e:
		print str(e)
		
		