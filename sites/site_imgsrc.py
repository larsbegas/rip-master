#!/usr/bin/python

from basesite import basesite
from bs4 import BeautifulSoup
import re

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
		self.debug('Sanitizing URL: ' + u)
		self.debug('self.original_url: ' + self.original_url)
		if "pwd=" in self.original_url:
			self.debug("pwd= in  %s" % self.original_url)
			pwd = self.original_url[self.original_url.find('pwd')+4:]
			self.imgsrcpwd = pwd
			self.debug("PWD: %s" % pwd)
		#print "1"
		if '?' in u:
			ad = u[u.find('?'):u.find('&')]
			u = u[:u.find('?')]
		self.debug('2')
		u = u.replace('http://', '').replace('https://', '')
		splits = u.split('/')
		self.debug("len splits %s " % len(splits))
		xxx = len(splits)
		self.debug(xxx)
		self.debug("** %s **" % " ".join(splits))
		if xxx>2:
			if  splits[2] == 'preword.php':
				self.debug("splits[2] == 'preword.php' url4:%s" % url)
				r = self.web.get(url)
				self.debug('4:%s' % r)
				#print "getting preword: %s \n" % r
				
				r2 = self.web.between(r, 'rel=shortlink', '>')
				r2b = self.web.between(r, '0xs.ru/', '\'')
				#print 5
				self.debug("r2: %s " % r2)
				self.debug("r2b: %s " % r2b)
				#assert(len(r2) > 0)
				u2 = r2[-1]
				#assert(len(u2) > 0)
				#print "u2 %s \n" % u2
				u3 = u2[7:-1]
				#print " r2: %s  " % r2[-1]
				if self.imgsrcpwd != '':
					u3 = u3 + '?pwd=' + self.imgsrcpwd
				self.debug(' u3: %s \n' % u3)
				
				return self.sanitize_url(u3)
		
		if ('0xs.ru' in splits):
			asd = 'http://' + '/'.join(splits)
			self.debug("\n0xs.ru 1:%s\n\n"%asd)
			if self.imgsrcpwd and self.imgsrcpwd != '':
				asd = asd + '?pwd=' + self.imgsrcpwd
			
			self.debug("\n\n0xs.ru 2:%s\n\n"%asd)
			return asd
		if len(splits) != 3 or \
				splits[1] == 'main' or \
				splits[2] == 'pic.php' or \
				splits[2] == 'pic_tape.php':
			if '0xs.ru' in splits:
				return 'http://' + '/'.join(splits)
			elif (pwd != '') and (ad) :
				return 'http://imgsrc.ru/main/pic_tape.php%s&pwd=%s' %  (ad, pwd)
			elif splits[2] == 'pic_tape.php':
				return 'http://imgsrc.ru/main/pic_tape.php%s&pwd=%s' %  (ad, pwd)
			raise Exception('invalid imgsrc url: expected <b>http://imgsrc.ru/&lt;user&gt;/&lt;album&gt;.html</b>')
		finret = 'http://imgsrc.ru/%s/%s?pwd=%s' % (splits[1], splits[2], pwd)
		self.debug('finret:%s'%finret)
		return finret
	
	""" Discover directory path based on URL """
	def get_dir(self, url):
		splits = url.split('/')
		self.debug(splits)
		#print '\n'
		if '.' in splits[-1]: splits[-1] = splits[-1][:splits[-1].find('.')]
		if splits[-2] == '0xs.ru':
			if self.username and (self.username != ''):
				return 'imgsrc_%s' % self.username
			else: return'imgsrc_%s' % (splits[-1])
			
		ret1 = (splits[-2])
		self.debug("returning:%s"%ret1)
		return 'imgsrc_%s' % ret1
	
	""" xxx """
	def get_gallery_dir(self, url, r='', gallno2=''):
		splits = url.split('/')
		self.debug("get_gallery_dir")
		self.debug(splits)
		gallno="asdasd"
		if 'pic_tape' in url:
			gallno = splits[3]
			self.debug("gallno = splits 3 :%s"%gallno)
		elif '.' in splits[-1]:
			splits[-1] = splits[-1][:splits[-1].find('.')]
			gallno = splits[-1]
		
		
		if r!='':
			gallnameArray = self.web.between(r, 'iMGSRC.RU</a> ','</td>')
			self.debug('GallnameArray: %s' % gallnameArray)
			
			if 'preword' in url:
				self.debug('preword gallno PRE: %s' % gallno)
				#window.location='http://imgsrc.ru/marsattacks/22394697.html?pwd=';
				#asdasd = self.web.between(r, "location=","html")
				re2 = re.match(r'/\w+/([^\.]+)\.html\?pwd', r, re.M|re.I)
				asdasd=""
				if re2:
					asdasd = re2.group(0)
				
				self.debug(asdasd)
				if asdasd:
					gallno =  asdasd
				else:
					self.debug(gallno2)
					gallno = gallno2
				
				self.debug('preword gallno AFTER: %s' % gallno)
				ret3 = gallno + " - " + gallnameArray[0] + " "
				self.debug('returning3:%s'%ret3)
				self.title = gallnameArray[0]
				return ret3
				#exit(gallno)
			
			self.debug('sadsdsad4444')
			ret1 = gallnameArray[0] + ' - ' + gallno + ' '
			self.title = gallno
			self.debug('returning1:%s'%ret1)
			return ret1
		
		self.debug('sadsdsaqqd2222')
		self.debug('returning gallno2: %s'%gallno2)
		self.title = gallno
		return gallno2
	
	def verify_r(self, r):
		self.debug("Verifiy?.. ")
		if "href='/main/warn.php" in r:
			# Need to verify age
			verify = self.web.between(r, "href='/main/warn.php", "'")[0]
			verify = 'http://imgsrc.ru/main/warn.php%s' % verify
			self.web.get(verify)
			r = self.web.get(self.url)
			self.debug("yea, verified")
		
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
			else: self.debug("link == None	")
		else:
			if (self.imgsrcpwd != "") and ('pwd' not in r):
				self.url = self.url + "&pwd=" + self.imgsrcpwd
			self.debug('VERIFY: no CONTINUE or main warn found continue to:%s'%self.url )
			r = self.web.get(self.url)
			#exit(r)
		
		
		return r

	def download(self, pwd=''):
		#self.debug("Start pre init")
		self.init_dir()
		#self.debug("Start post init")
		myurl = self.original_url
		if pwd!='':
			self.url = self.original_url
			r = self.web.get(self.original_url)
			r = self.verify_r(r)
		else:
			r = self.web.get(self.url)
			
			r = self.verify_r(r)
			# Load full-page gallery to save time

			atemp_url = self.web.between(r, "href='/main/pic_tape.php?ad=", '\'')[0]
			if atemp_url.endswith('&pwd='):
				atemp_url = atemp_url[:atemp_url.find('&')]
			self.debug("atemp: %s " % atemp_url)
			
			temp_url = "HHHHHHHH"
			if atemp_url:
				if isinstance(atemp_url, list):
					temp_url = atemp_url[0]
				else: temp_url = atemp_url
			else: raise Exception("pictape fehlt wohl sieh hier")
			self.url = 'http://imgsrc.ru/main/pic_tape.php?ad=%s' % temp_url
			self.debug("end download() self.url: %s " % self.url)
			r = self.web.get(self.url)
		
		if not "pic_tape.php" in self.url:
			print 'could not find pic_tape.php in %s' % self.url
			self.wait_for_threads()
			raise Exception('could not find pic_tape.php in %s' % self.url)
		
		
		#self.debug("rr: %s" % r)
		
		skip_amount = 12
		current     = 0
		img_index   = 0
		img_total   = 0
		
		while True:
			self.debug("while true:")
			#self.debug("RRRR: %s" % r)
			links = self.web.between(r, 'class="big" src=\'', "'")
			self.debug("LINKS1:")
			self.debug(links)
			img_total += len(links)
			
			#print "LINKS"
			#print links
			
			if len(links) <= 0:
				raise Exception("88")
			
			for link2 in links:
				self.debug("UUUU2 liunk:%s" % link2)
				splits2 = link2.split('/')
				self.debug(splits2)
				img_index += 1
				saveas="U1-G1-"
				gallname2=""
				try:
					if '.ru/m/' in link2:
						
						gallname2 = self.get_gallery_dir(myurl, r)
						saveas = splits2[4] + " - " + gallname2 + " "
						self.debug('saveasYY: ' + saveas)
					else:
						saveas = link2[link2.rfind('/')+1:]
						self.debug('saveasZZ: ' + saveas)
						gallname2 = self.get_gallery_dir(myurl, r)
						
						saveas = gallname2 + ' - ' + saveas
						self.debug('saveasXX: ' + saveas)
				except Exception, e:
					self.debug(e)
				
				if '?' in saveas: saveas = saveas[:saveas.find('?')]
				saveas = re.sub('[.!/#:]', '', saveas)
				self.debug('now base->down saveas:%s link2:%s gallname2:%s ' \
					% (saveas, link2, gallname2))
				self.download_image(link2, img_index, total=img_total, subdir='', saveas=saveas)
				#if self.hit_image_limit(): break
			#if self.hit_image_limit(): break
			if '>next ' not in r: break
			current += skip_amount
			r = self.web.get('%s&way=&skp=%d&pwd=%s' % (self.url, current, pwd))
		self.wait_for_threads()
	
