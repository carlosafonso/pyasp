import os
import requests

class Pyasp(object):
	DEFAULT_COOKIEJAR = "/tmp/pyasp.cookiejar"

	def __init__(self, cookiejar=DEFAULT_COOKIEJAR):
		self.cookiejar = cookiejar

	def get(self, url):
		return requests.get(url)

	def post(self, url):
		return requests.post(url)