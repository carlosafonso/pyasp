import os
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

	def __request(self, method, url):
		methods = {'get': requests.get, 'post': requests.post}

		response = methods[method](url)
		try:
			soup = BeautifulSoup(response.text)

			tag = soup.find('input', {'name': '__VIEWSTATE'})
			if tag is not None:
				self.viewstates = [tag['value']]
		except TypeError:
			pass

		return response