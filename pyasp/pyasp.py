import os
import re
import requests

from bs4 import BeautifulSoup

class Pyasp(object):
	DEFAULT_COOKIEJAR = "/tmp/pyasp.cookiejar"

	def __init__(self, cookiejar=DEFAULT_COOKIEJAR):
		self.cookiejar = cookiejar
		self.viewstates = []
		self.eventvalidation = None

	def get(self, url):
		return self.__request(method='get', url=url)

	def post(self, url):
		return self.__request(method='post', url=url)

	def put(self, url):
		return self.__request(method='put', url=url)

	def __request(self, method, url):
		methods = {'get': requests.get, 'post': requests.post, 'put': requests.put}

		response = methods[method](url)
		try:
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