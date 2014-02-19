#!/usr/bin/python

from sys import exit
import sys
import re

from site_imgsrc       import imgsrc
from site_imgur       import imgur
from site_deviantart  import deviantart
from site_photobucket import photobucket
from site_flickr      import flickr
from site_twitter     import twitter
from site_tumblr      import tumblr
from site_instagram   import instagram
from site_imagefap    import imagefap
from site_imagebam    import imagebam
from site_imgsrc      import imgsrc
from site_imagearn    import imagearn
from site_xhamster    import xhamster
from site_getgonewild import getgonewild
from site_anonib      import anonib
from site_motherless  import motherless
from site_4chan       import fourchan
from site_occ         import occ
from site_minus       import minus
from site_gifyo       import gifyo
from site_imgsrc      import imgsrc
from site_five00px    import five00px
from site_chickupload import chickupload
from site_cghub       import cghub
from site_teenplanet  import teenplanet
from site_chansluts   import chansluts
from site_gonearch    import gonearch
from site_chanarchive import chanarchive
from site_seenive	  import seenive
from site_vinebox	  import vinebox
from site_webstagram  import   webstagram
from site_statigram   import   statigram

from Httpy import Httpy

def down(gall):
	if 'imagefap' in gall:
		i = imagefap(gall, debugging=True)
	elif('seenive' in gall):
		i = seenive(gall, debugging=True)
	elif('vinebox' in gall):
		i = vinebox(gall, debugging=True)
	elif('sta.tigram' in gall):
		i = statigram(gall, debugging=True)
	elif('web.stagram.com' in gall):
		i = webstagram(gall, debugging=True)
	elif('instagram.com' in gall):
		i = instagram(gall, debugging=True)
	elif('imgsrc.ru' in gall):
		i = imgsrc(gall, debugging=True)
	else:
		exit('not found ripper for %s' % gall)
	print "Working_dir: %s url: %s" % (i.working_dir, i.url)

	#if("?pwd=&" in gall):
		#gall = gall[gall.find("\?pwd=&")]
		#(gall)
		
	#if i.existing_zip_path() != None:
	#	print 'Zip exists: %s' % i.existing_zip_path()
	#else:
	try:
		print 'downloading...'
		if ('pic_tape' in gall):
			pwd = i.original_url[i.original_url.find('&')+5:]
			print "PWD: %s" % pwd
			i.download(pwd=pwd)
		else:
			i.download()
		return True
		#success.append(gall)
	except  Exception, e1:
		print 'Exception while Downloading: %s' % str(e1)
		#failed.append(gall)
		return False
	
	'''	
	print 'checking for zip:',
	print str(i.existing_zip_path())
	print "zip = %s" % i.zip()
	print 'checking for zip:',
	print str(i.existing_zip_path())
	if i.existing_zip_path().endswith('.txt'):
	    f = open(i.existing_zip_path(), 'r')
	    print f.read()
	    f.close()
	    '''
	
try:
    #i = imgsrc('http://imgsrc.ru/martin1989/a1022028.html?', debugging=True)
    #i = imgsrc('http://imgsrc.ru/martin1989/a1003277.html?', debugging=True)
    #i = imgsrc('http://imgsrc.ru/martin1989/a1021809.html?', debugging=True)
    #i = imgsrc('http://imgsrc.ru/main/pic_tape.php?ad=678965&pwd=bbe4233b74a1ca3ca6ba0c0c84bfe12e', debugging=True)
	failed = []
	success = []
	#failed.add("asd")
	print sys.argv
	for gall in sys.argv:
		if (gall.endswith("test.py")):
			continue
		else: print "START: gall: %s \n" % gall


		i = None
		gs = gall.split('/')
		print gs
		'''
		http://www.imagefap.com/profile/immerspass2/galleries?folderid=-1
		
		'''
		httpy = Httpy()
		
		rGallKat = re.compile('http://www.imagefap.com/profile/([^\/]*)/galleries\?folderid=-?(\d+)') 
		
		if rGallKat.match(gall):
			#r = httpy.get('http://www.imagefap.com/profile/%s/galleries?folderid=' %gs[4])
			r = httpy.get(gall)
			galls = set()
			
			gallpat = re.compile('\/gallery\/(\d+)')
			for b in re.findall(gallpat, r):
				print b
				galls.add(b)
			
			print "galls:%s"%str(galls)
			for z in galls:
				z = "http://imagefap.com/gallery/%s" % z
				if down(z): 
					success.append(z) 
				else: 
					failed.append(z)
			continue
				
		if down(gall):
			success.append(gall)
		else: 
			failed.append(gall)
			
	print '\n+++++++ ENDE ++++++++++\n'
	for su in success:
		print('success: %s' % su)
	for fail in failed:
		print('failed: %s' % fail)
	
	
except Exception, e:
    print "\nEXCEPTION: %s" % str(e)
