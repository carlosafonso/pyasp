import os

class Pyasp(object):
	DEFAULT_COOKIEJAR = "/tmp/pyasp.cookie.jar"

	def __init__(self, cookiejar=DEFAULT_COOKIEJAR):
		self.cookiejar = cookiejar