import os
import re
import requests

from bs4 import BeautifulSoup

class Pyasp(object):
	def __init__(self):
		self.viewstates = []
		self.eventvalidation = None

	def get(self, url, headers=None):
		return self.__request(method='get', url=url, headers=headers)

	def post(self, url, headers=None):
		return self.__request(method='post', url=url, headers=headers)

	def put(self, url, headers=None):
		return self.__request(method='put', url=url, headers=headers)

	def __request(self, method, url, headers=None):
		# all available HTTP methods
		methods = {'get': requests.get, 'post': requests.post, 'put': requests.put}
		
		if headers is None:
			headers = {}
		
		# add any captured __VIEWSTATE field to POST requests only
		if method == 'post':
			if len(self.viewstates) == 1:
				headers['__VIEWSTATE'] = self.viewstates[0]
			elif len(self.viewstates) > 1:
				for idx, viewstate in enumerate(self.viewstates):
					headers['__VIEWSTATE{}'.format(idx + 1)] = self.viewstates[idx]

			if self.eventvalidation is not None:
				headers['__EVENTVALIDATION'] = self.eventvalidation

		# issue the request
		response = methods[method](url, headers=headers)

		# parse any __VIEWSTATE and __EVENTVALIDATION fields
		try:
			self.viewstates = []
			self.eventvalidation = None

			soup = BeautifulSoup(response.text)

			viewstate_tags = soup.find_all('input', {'name': re.compile('__VIEWSTATE(\d+)?')})
			if len(viewstate_tags):
				for tag in viewstate_tags:
					self.viewstates.append(tag['value'])

			eventvalidation_tag = soup.find('input', {'name': '__EVENTVALIDATION'})
			if eventvalidation_tag is not None:
				self.eventvalidation = eventvalidation_tag['value']

		except TypeError:
			pass

		return response