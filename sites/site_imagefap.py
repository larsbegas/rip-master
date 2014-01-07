#!/usr/bin/python

from basesite import basesite
from bs4 import BeautifulSoup
import re

"""
	Downloads imagefap albums
"""
class imagefap(basesite):
	"""
		Ensure URL is relevant to this ripper.
		Return 'sanitized' URL (if needed).
	"""
	def sanitize_url(self, url):
		#print url
		if not 'imagefap.com/' in url: 
			raise Exception('')
		gid = self.get_gid(url)
		if gid == '':
			raise Exception('?gid= and /pictures/ and /gallery/not found in URL')
		return 'http://www.imagefap.com/gallery.php?gid=%s&view=2' % gid

	""" Extract gallery id from URL. Return empty string if not found """
	def get_gid(self, url):
		gid = ''
		for before in ['?gid=', '/pictures/','/gallery/']:
			if before in url:
				gid = url[url.rfind(before)+len(before):]
		for c in ['/', '?', '#', '&']:
			if c in gid: gid = gid[:gid.find(c)]
		
		return gid

	""" Discover directory path based on URL """
	def get_dir(self, url):
		return 'imagefap_%s' % self.get_gid(url)
		#return 'IMAGEFAP' #% self.get_gid(url)

	def download(self):
		self.init_dir()
		r = self.web.get(self.url)
		soup = BeautifulSoup(r)
		title = str(soup.title)
		title = title[20:-8]
		title = title.rstrip()
		title = title.replace('\/', '_')
		if ('(Page') in title:
			title = title[:title.find('(')]
		#title = self.web.between(r, 'Porn pics of ', '[(<\(]')
		user = self.web.between(r, 'Uploaded by ', '<')
		username = user.pop()
		
		r = r[r.find('showMoreGalleries'):] # To ignore user icon
		links = self.web.between(r, 'fap.to/images/thumb/', '"')
		self.debug('title:%s' % title)
		self.debug('user:%s' % username)		
		
		for (index, link) in enumerate(links):
			pid = link[7:-4]
			ext = link[-3:]
			saveas = username + ' - ' + title + ' (' + pid + ').' + ext
			self.debug('Saveas:%s' % saveas)
			link = 'http://fap.to/images/full/%s' % link
			self.download_image(link, index + 1, total=len(links), saveas=saveas, subdir=username)
			if self.hit_image_limit(): break
		self.wait_for_threads()
