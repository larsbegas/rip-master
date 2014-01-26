#!/usr/bin/python

from basesite import basesite

"""
	Downloads instagram albums
"""
class webstagram(basesite):
	
	""" Parse/strip URL to acceptable format """
	# http://web.stagram.com/n/izabelle12123
	def sanitize_url(self, url):
		if'web.stagram.com/n/' in url:
			# Legit
			self.debug("LEGIT websta: " + url)
			pass
		elif '___instagram.com/' in url:
			# Convert to web.stagram
			user = url[url.find('.com/')+len('.com/'):]
			if '/' in user: user = user[:user.find('/')]
			url = 'http://web.stagram.com/n/%s' % user
		elif 'pinsta.me/' in url:
			# Convert to web.stagram
			user = url[url.find('.me/')+len('.me/'):]
			if '/' in user: user = user[:user.find('/')]
			url = 'http://web.stagram.com/n/%s' % user
		else:
			raise Exception('')
		#if '?' in url: url = url[:url.find('?')]
		#if '#' in url: url = url[:url.find('#')]
		self.debug('sani websta returning: %s' % url)
		return url

	""" Discover directory path based on URL """
	def get_dir(self, url):
		user = url[url.find('.com/n/')+len('.com/n/'):]
		if '/' in user: user = user[:user.find('/')]
		return 'instagram_%s' % user

	def download(self):
		self.init_dir()
		r = self.web.get(self.url)
		with open("webstaDownloadR.html", "w") as text_file:
		    text_file.write("r:%s"%r)
		totals = self.web.between(r, 'font-size:123.1%;">', '<')
		if len(totals) > 0: total = int(totals[-1])
		else: total = -1
		index = 0
		
		self.debug('websta download totals:%d' %total)
		while True:
			chunks = self.web.between(r, '<div class="infolist">', '<div class="like_comment')
			self.debug('websta down chunks:%s'%len(chunks))
			for chunk in chunks:
				imgs = self.web.between(chunk, '<a href="', '"')
				if len(imgs) < 4: continue
				img = imgs[3].replace('_6.', '_8.')
				self.debug('found img: %s' % img)
				if '<div class="hasvideo' in chunk:
					vid = img.replace('_8.jpg', '_101.mp4')
					self.debug('video found, url: %s' % vid)
					meta = self.web.get_meta(vid)
					if 'Content-Length' in meta and meta['Content-Length'] != '0' and \
						'Content-Type' in meta and 'video' in meta['Content-Type']:
						self.debug('meta shows vid is legit')
						img = vid
					else:
						self.debug('meta shows vid is not legit')
				
				index += 1
				self.download_image(img, index, total=total) 
				if self.hit_image_limit(): break
			if self.hit_image_limit(): break
			earliers = self.web.between(r, ' [ <a href="/n/', '"')
			if len(earliers) != 2: break
			r = self.web.get('http://web.stagram.com/n/%s' % earliers[0])
		self.wait_for_threads()
	
