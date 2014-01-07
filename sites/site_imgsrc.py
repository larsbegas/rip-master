#!/usr/bin/python

from basesite import basesite
from bs4 import BeautifulSoup

class imgsrc(basesite):
	
	# http://imgsrc.ru/main/pic.php?ad=774665
	# http://imgsrc.ru/jp101091/26666184.html?pwd=&lang=en#
	# http://imgsrc.ru/fotoivanov/a661729.html
	""" Parse/strip URL to acceptable format """
	def sanitize_url(self, url):
		if (not 'imgsrc.ru/' in url) and (not '0xs.ru/' in url):
			#print "\n\nURL:%s" % url
			raise Exception('')
		u = url
		pwd = ''
		#print 'Sanitizing URL: ' + u
		#print 'self.original_url: ' + self.original_url
		if '&pwd=' in self.original_url:
			pwd = self.original_url[self.original_url.find('&')+5:]
			#print "PWD: %s" % pwd
		#print "1"
		if '?' in u:
			ad = u[u.find('?'):u.find('&')]
			u = u[:u.find('?')]
		#print '2'
		u = u.replace('http://', '').replace('https://', '')
		splits = u.split('/')
		#print "len splits %s " % len(splits)
		xxx = len(splits)
		#print xxx
		if xxx>2:
			#print "********** %s" % "k".join(splits)
			if  splits[2] == 'preword.php':
				#print url
				r = self.web.get(url)
				#print '4:%s' % r
				#print "getting preword: %s \n" % r
				
				r2 = self.web.between(r, 'rel=shortlink', '>')
				#print 5
				#print "r2: %s " % r2
				#assert(len(r2) > 0)
				u2 = r2[-1]
				#assert(len(u2) > 0)
				#print "u2 %s \n" % u2
				u3 = u2[7:-1]
				#print " r2: %s  " % r2[-1]
				#print ' u3: %s \n' % u3
				
				return self.sanitize_url(u3)
		
		if ('0xs.ru' in splits):
			#print "ajksbdakjsbdf\n\n\n"
			return 'http://' + '/'.join(splits)
		if len(splits) != 3 or \
				splits[1] == 'main' or \
				splits[2] == 'pic.php' or \
				splits[2] == 'pic_tape.php':
			if '0xs.ru' in splits:
				return 'http://' + '/'.join(splits)
			elif (pwd != '') and (ad) :
				return 'http://imgsrc.ru/main/pic_tape.php%s&pwd=%s' %  (ad, pwd)
			elif splits[2] == 'pic_tape.php':
				return 'http://imgsrc.ru/main/pic_tape.php%s' %  ad
			raise Exception('invalid imgsrc url: expected <b>http://imgsrc.ru/&lt;user&gt;/&lt;album&gt;.html</b>')
		return 'http://imgsrc.ru/%s/%s?%s' % (splits[1], splits[2], pwd)
	
	""" Discover directory path based on URL """
	def get_dir(self, url):
		splits = url.split('/')
		#print splits
		#print '\n'
		if '.' in splits[-1]: splits[-1] = splits[-1][:splits[-1].find('.')]
		if splits[-2] == '0xs.ru':
			return'imgsrc_%s' % (splits[-1])
		return 'imgsrc_%s' % (splits[-2])
	
	""" xxx """
	def get_gallery_dir(self, url, r=''):
		splits = url.split('/')
		if '.' in splits[-1]: splits[-1] = splits[-1][:splits[-1].find('.')]
		gallno = splits[-1]
		if r!='':
			if 'preword' in gallno:
				gallno =  self.web.between(r, 'href=/michi1000/','.html')[0]
				#exit(gallno)
			
			gallnameArray = self.web.between(r, 'iMGSRC.RU</a> ','</td>')
			#print 'GallnameArray: %s' % gallnameArray
			#print '\n'
			
			return gallnameArray[0] + ' - ' + gallno + ''
		return gallno
	
	def verify_r(self, r):
		#print "Verifiy?.. "
		if "href='/main/warn.php" in r:
			# Need to verify age
			verify = self.web.between(r, "href='/main/warn.php", "'")[0]
			verify = 'http://imgsrc.ru/main/warn.php%s' % verify
			self.web.get(verify)
			r = self.web.get(self.url)
			#print "yea, verified"
		
		#if 'Please enter album\'s password' in r:
			#self.wait_for_threads()
			#raise Exception('album is password protected')
		
		
		elif "Continue to album" in r:
			s = BeautifulSoup(r)
			link = s.find('a', text='Continue to album &gt;&gt;')
			#for linka in s.find_all('a'):
			#	self.debug(linka)
			
			if link != None:
				self.log('Continue to album: ' + link)
				r = self.web.get(link.href)
			else: self.debug("dasddasd	")
		else: self.debug('no')
		
		return r
	
	def download(self, pwd=''):
		self.debug("Start dling")
		self.init_dir()
		myurl = self.original_url
		if pwd!='':
			self.url = self.original_url
			r = self.web.get(self.original_url)
			#print "download() pwd set: url %s\n " % self.original_url
			r = self.verify_r(r)
		
		else:
			r = self.web.get(self.url)
			
			r = self.verify_r(r)
			
			# Load full-page gallery to save time
			temp_url = self.web.between(r, "href='/main/pic_tape.php?ad=", '\'')[0] #was '&'
			self.url = 'http://imgsrc.ru/main/pic_tape.php?ad=%s' % temp_url
			#print "uuuuuu %s " % self.url
			r = self.web.get(self.url)
		
		if not "href='/main/pic_tape.php?ad=" in r and False:
			#print "RRRR_: %s" % r
			#exit()
			self.wait_for_threads()
			raise Exception('could not find "view all images" link')
		
		
		#print "RRRR: %s" % r
		
		skip_amount = 12
		current     = 0
		img_index   = 0
		img_total   = 0
		
		while True:
			#print "while true: %s" % r
			links = self.web.between(r, 'class="big" src=\'', "'")
			img_total += len(links)
			
			#print "LINKS"
			#print links
			
			if len(links) <= 0:
				#print r
				exit(88)
			for link2 in links:
				self.debug("UUUU2 liunk:%s" % link2)
				img_index += 1
				saveas="U1-G1-"
				try:
					saveas = link2[link2.rfind('/')+1:]
					gallname2="";
					if (not False):
						gallname2 = self.get_gallery_dir(myurl, r)
					else: gallname2 = "USER-GALL-"
					saveas = gallname2 + ' - ' + saveas
					self.log('saveas: ' + saveas)
				except: pass
				
				if '?' in saveas: saveas = saveas[:saveas.find('?')]
				if ':' in saveas: saveas = saveas[:saveas.find(':')]
				self.download_image(link2, img_index, total=img_total, subdir='', saveas=saveas)
				if self.hit_image_limit(): break
			if self.hit_image_limit(): break
			if '>next ' not in r: break
			current += skip_amount
			r = self.web.get('%s&way=&skp=%d&pwd=%s' % (self.url, current, pwd))
		self.wait_for_threads()
	
