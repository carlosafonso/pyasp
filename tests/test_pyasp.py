import mock
import os
import pytest
import unittest

from pyasp.pyasp import Pyasp

class TestPyasp(unittest.TestCase):
	def setup_method(self, method):
		self.pyasp = Pyasp()

	def test_default_cookie_jar(self):
		"""Does the library use the default cookie
		jar file if none is specified?"""
		assert self.pyasp.cookiejar == Pyasp.DEFAULT_COOKIEJAR

	def test_custom_cookie_jar(self):
		"""Does the library use the specified cookie
		jar file if one is provided?"""
		self.pyasp = Pyasp(cookiejar="/tmp/customjar")

		assert self.pyasp.cookiejar == "/tmp/customjar"

	@mock.patch('pyasp.pyasp.requests')
	def test_get(self, mock_requests):
		url = "http://anyurl"

		response = self.pyasp.get(url)

		mock_requests.get.assert_called_with(url)

	@mock.patch('pyasp.pyasp.requests')
	def test_post(self, mock_requests):
		url = "http://anyurl"

		response = self.pyasp.post(url)
		
		mock_requests.post.assert_called_with(url)