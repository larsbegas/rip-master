#!/usr/bin/python

from basesite import basesite
from json import loads, dumps
from time import sleep
from os   import path

from instagram.client import InstagramAPI
"""
	Downloads instagram albums
"""
class instagram(basesite):
	
	def login2(self):
		self.debug("11111")
		access_token = ('648417338.21874d4.8baa4d5f48064ee1873c6ecdc5ecb0d3', {'username': 'kiliianpauli', 'bio': u'Schule vorbei, jetzt Info studieren. Mache semiprof edits, mit cutten und Ebenen. Auf insta aber #100%BS @KiliiArt f\xfcr eigene edit', 'website': u'', 'profile_picture': 'http://images.ak.instagram.com/profiles/profile_648417338_75sq_1389753438.jpg', 'full_name': 'Kilian Paul', 'id': '648417338'})
		#('648417338.21874d4.8baa4d5f48064ee1873c6ecdc5ecb0d3', {'username': 'kiliianpauli', 'bio': u'Schule vorbei, jetzt Info studieren. Mache semiprof edits, mit cutten und Ebenen. Auf insta aber #100%BS @KiliiArt f\xfcr eigene edit', 'website': u'', 'profile_picture': 'http://images.ak.instagram.com/profiles/profile_648417338_75sq_1389753438.jpg', 'full_name': 'Kilian Paul', 'id': '648417338'})
		self.api = InstagramAPI(access_token=access_token)
		self.debug("api: %s" %str(self.api))
		#r = self.web.get('https://api.instagram.com/v1/users/self/media/liked?access_token=648417338.1fb234f.21e965466dad4d76857a001a99e55a4a')
		#exit(r) 
		''''
		recent_media, next = api.user_recent_media(user_id="@kiliianpauli", count=10)
		self.debug("333333")
		for media in recent_media:
		   print media.caption.text
		   
		exit("asd")
		'''
		
	def login(self):
		client_id = self.get_api_key()
		url = "https://api.instagram.com/oauth/authorize/?client_id=%s&redirect_uri=mbook.local&response_type=code"%client_id
		baseurl = '%s/media?client_id=%s' % (self.url, client_id)
		r = self.web.post(url)
		exit(r)
		
	""" Retrieves API key from local file """
	def get_api_key(self):
		api_path = path.join(path.dirname(__file__), 'instagram_api.key')
		api_key = ''
		if path.exists(api_path):
			f = open(api_path, 'r')
			api_key = f.read().replace('\n', '').strip()
			f.close()
		if api_key == '':
			raise Exception('no instagram API key found at %s' % api_path)
		return api_key

	""" Parse/strip URL to acceptable format """
	def sanitize_url(self, url):
		if'instagram.com/' in url:
			# Legit
			pass
		elif 'XXXXXXweb.stagram.com/n/' in url:
			# Convert to web.stagram
			user = url[url.find('.com/n/')+len('.com/n/'):]
			if '/' in user: user = user[:user.find('/')]
			url = 'http://instagram.com/%s' % user
		else:
			raise Exception('')
		if '?' in url: url = url[:url.find('?')]
		if '#' in url: url = url[:url.find('#')]
		while url.endswith('/'): url = url[:-1]
		return url

	""" Discover directory path based on URL """
	def get_dir(self, url):
		user = url[url.rfind('/')+1:]
		return 'instagram_%s' % user

	def download(self):
		self.login2()
		self.init_dir()
		#client_id = self.get_api_key()
		#baseurl = '%s/media?client_id=%s' % (self.url, client_id)
		#self.debug('baseurl:%s' % baseurl)
		#url = baseurl
		index = 0
		# url = self.web.get('https://api.instagram.com/v1/users/376399567/follows?access_token=648417338.1fb234f.21e965466dad4d76857a001a99e55a4a')
		# url = self.web.get('https://api.instagram.com/v1/users/self/feed?access_token=648417338.1fb234f.21e965466dad4d76857a001a99e55a4a')
		url = self.web.get('https://api.instagram.com/v1/users/376399567/media/recent?access_token=648417338.1fb234f.21e965466dad4d76857a001a99e55a4a')
		while True:
			#self.debug('loading %s' % url)
			#r = self.web.get(url)
			try: json = loads(url)
			except:
				self.wait_for_threads()
				self.debug('invalid json response:\n%s' % url)
				#raise Exception('unable to parse json at %s' % url)
				break
				
			#if not json['meta']['code'] == 200:
				#exit(json['meta'])
				#self.wait_for_threads()
			#	self.log('meta: %s' % str(json['meta']))
			#	break
			#	#raise Exception('meta not "ok": %s' % str(json['meta']))
			
			''''
			for item in json['data']:
				username = item['username']
				last_id = item['id']
				self.debug(username)
				continue
				
				for media_type in ['videos', 'images']:
					if not media_type in item: continue
					index += 1
					media_url = item[media_type]['standard_resolution']['url']
					self.download_image(media_url, index)
					sleep(0.5)
					break
			'''
			if 'data' in json.keys():
				for d in json['data']:
					index += 1
					medid = d['id']
					self.debug(medid)
					mediaj = self.web.get('https://api.instagram.com/v1/media/' + \
						str(medid) + '?access_token=648417338.1fb234f.21e965466dad4d76857a001a99e55a4a')
					self.download_image(mediaj, index)
				#self.debug(dumps(data))
				
				
			self.debug("Sleep..")
			sleep(1)
			self.debug("..Done")
			
			
			pag = json['pagination']
			if pag != None:
				if 'next_url' in pag.keys():
					nu = pag['next_url']
					try:
						url = self.web.get(nu)
					except:
						break												
					continue
				else:
					break
			else:
				break
			''''
			last_id = 0
			#self.debug(json)
			#exit(nu)
			for item in json['data']:
				username = item['username']
				last_id = item['id']
				self.debug(username)
				continue
				
				for media_type in ['videos', 'images']:
					if not media_type in item: continue
					index += 1
					media_url = item[media_type]['standard_resolution']['url']
					self.download_image(media_url, index)
					sleep(0.5)
					break
				if self.hit_image_limit(): break
			if self.hit_image_limit(): break
			if not json['more_available'] or last_id == 0: break
			sleep(2)
			url = '%s&max_id=%s' % (baseurl, last_id)
			'''
		self.wait_for_threads()
	
