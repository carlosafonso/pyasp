import mock
import os
import pytest
import responses
import unittest

from pyasp.pyasp import Pyasp

class TestPyasp(unittest.TestCase):
	ANY_URL = "http://anyurl"
	ANY_RESPONSE_BODY = "<html><body></body></html>"
	SAMPLE_B64 = "ZmluZ2VycyBjcm9zc2VkLCB0aGlzIHRlc3Qgc2hhbGwgbm90IGZhaWwh"

	def setup_method(self, method):
		self.pyasp = Pyasp()
		responses.reset()

	def test_default_cookie_jar(self):
		"""Does the library use the default cookie
		jar file if none is specified?"""
		assert self.pyasp.cookiejar == Pyasp.DEFAULT_COOKIEJAR

	def test_custom_cookie_jar(self):
		"""Does the library use the specified cookie
		jar file if one is provided?"""
		self.pyasp = Pyasp(cookiejar="/tmp/customjar")

		assert self.pyasp.cookiejar == "/tmp/customjar"

	def test_state_vars_empty_on_init(self):
		"""Are all state variables correctly initialized?"""
		assert self.pyasp.viewstates == []
		assert self.pyasp.eventvalidation == None

	@mock.patch('pyasp.pyasp.requests')
	def test_get(self, mock_requests):
		"""Are GET requests being issued correctly?"""
		url = TestPyasp.ANY_URL

		self.pyasp.get(url)
		
		mock_requests.get.assert_called_with(url)

	@mock.patch('pyasp.pyasp.requests')
	def test_post(self, mock_requests):
		"""Are POST requests being issued correctly?"""
		url = TestPyasp.ANY_URL

		self.pyasp.post(url)
		
		mock_requests.post.assert_called_with(url)

	@responses.activate
	def test_single_viewstate_parsing(self):
		"""Does the library correctly parse a single
		__VIEWSTATE field?"""
		responses.add(
			responses.GET, TestPyasp.ANY_URL,
			body='<html><body><input type="hidden" name="__VIEWSTATE" value="{}"/></body></html>'.format(TestPyasp.SAMPLE_B64))

		self.pyasp.get(TestPyasp.ANY_URL)

		assert len(self.pyasp.viewstates) == 1
		assert self.pyasp.viewstates[0] == TestPyasp.SAMPLE_B64

