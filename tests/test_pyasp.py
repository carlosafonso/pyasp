import mock
import os
import pytest
import responses
import unittest

from pyasp.pyasp import Pyasp

class TestPyasp(unittest.TestCase):
	ANY_URL = "http://anyurl"
	ANY_URL_2 = "http://anyurl2"
	ANY_RESPONSE_BODY = "<html><body></body></html>"
	SAMPLE_B64 = "ZmluZ2VycyBjcm9zc2VkLCB0aGlzIHRlc3Qgc2hhbGwgbm90IGZhaWwh"
	SAMPLE_B64_2 = "eW91ciBhZCBoZXJlISBjb250YWN0IHVzIQ=="

	def setup_method(self, method):
		self.pyasp = Pyasp()
		responses.reset()

	def test_state_vars_empty_on_init(self):
		"""Are all state variables correctly initialized?"""
		assert self.pyasp.viewstates == []
		assert self.pyasp.eventvalidation == None

	@mock.patch('pyasp.pyasp.requests')
	def test_get(self, mock_requests):
		"""Are GET requests being issued correctly?"""
		url = TestPyasp.ANY_URL

		self.pyasp.get(url)
		
		mock_requests.get.assert_called_with(url, headers={})

	@mock.patch('pyasp.pyasp.requests')
	def test_post(self, mock_requests):
		"""Are POST requests being issued correctly?"""
		url = TestPyasp.ANY_URL

		self.pyasp.post(url)
		
		mock_requests.post.assert_called_with(url, headers={})

	@mock.patch('pyasp.pyasp.requests')
	def test_put(self, mock_requests):
		"""Are PUT requests being issued correctly?"""
		url = TestPyasp.ANY_URL

		self.pyasp.put(url)
		
		mock_requests.put.assert_called_with(url, headers={})

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

	@responses.activate
	def test_multiple_viewstate_parsing(self):
		"""Does the library correctly parse several
		__VIEWSTATE fields?"""
		responses.add(
			responses.POST, TestPyasp.ANY_URL,
			body='<html><body><input type="hidden" name="__VIEWSTATE1" value="{}"/>' \
				'<input type="hidden" name="__VIEWSTATE2" value="{}"/></body></html>'.format(TestPyasp.SAMPLE_B64, TestPyasp.SAMPLE_B64_2))

		self.pyasp.post(TestPyasp.ANY_URL)

		assert len(self.pyasp.viewstates) == 2
		assert self.pyasp.viewstates[0] == TestPyasp.SAMPLE_B64
		assert self.pyasp.viewstates[1] == TestPyasp.SAMPLE_B64_2

	@responses.activate
	def test_eventvalidation_parsing(self):
		"""Does the library correctly parse the
		__EVENTVALIDATION field?"""
		responses.add(
			responses.GET, TestPyasp.ANY_URL,
			body='<html><body><input type="hidden" name="__EVENTVALIDATION" value="{}"/></body></html>'.format(TestPyasp.SAMPLE_B64))

		self.pyasp.get(TestPyasp.ANY_URL)

		assert self.pyasp.eventvalidation == TestPyasp.SAMPLE_B64

	@mock.patch('pyasp.pyasp.requests')
	def test_single_viewstate_is_not_sent_on_get(self, mock_requests):
		"""Does the library skip a single parsed
		__VIEWSTATE field when issuing a GET request?"""
		url = TestPyasp.ANY_URL
		self.pyasp.viewstates.append(TestPyasp.SAMPLE_B64)

		self.pyasp.get(TestPyasp.ANY_URL)

		with pytest.raises(AssertionError):
			mock_requests.get.assert_called_with(url, headers={'__VIEWSTATE': TestPyasp.SAMPLE_B64})

	@mock.patch('pyasp.pyasp.requests')
	def test_eventvalidation_is_not_sent_on_get(self, mock_requests):
		"""Does the library skip the __EVENTVALIDATION
		field when issuing a GET request?"""
		url = TestPyasp.ANY_URL
		self.pyasp.eventvalidation = TestPyasp.SAMPLE_B64

		self.pyasp.get(TestPyasp.ANY_URL)

		with pytest.raises(AssertionError):
			mock_requests.get.assert_called_with(url, headers={'__EVENTVALIDATION': TestPyasp.SAMPLE_B64})
		

	@mock.patch('pyasp.pyasp.requests')
	def test_single_viewstate_is_sent_on_post(self, mock_requests):
		"""Does the library send a single parsed 
		__VIEWSTATE field when issuing a POST request?"""
		url = TestPyasp.ANY_URL
		self.pyasp.viewstates.append(TestPyasp.SAMPLE_B64)

		self.pyasp.post(TestPyasp.ANY_URL)

		mock_requests.post.assert_called_with(url, headers={'__VIEWSTATE': TestPyasp.SAMPLE_B64})

	@mock.patch('pyasp.pyasp.requests')
	def test_multiple_viewstates_are_sent_on_post(self, mock_requests):
		"""Does the library send all parsed __VIEWSTATE
		fields when issuing a POST request?"""
		url = TestPyasp.ANY_URL
		self.pyasp.viewstates.append(TestPyasp.SAMPLE_B64)
		self.pyasp.viewstates.append(TestPyasp.SAMPLE_B64_2)

		self.pyasp.post(TestPyasp.ANY_URL)

		mock_requests.post.assert_called_with(url,
			headers={'__VIEWSTATE1': TestPyasp.SAMPLE_B64, '__VIEWSTATE2': TestPyasp.SAMPLE_B64_2})

	@mock.patch('pyasp.pyasp.requests')
	def test_eventvalidation_is_sent_on_post(self, mock_requests):
		"""Does the library send the __EVENTVALIDATION
		field when issuing a POST request?"""
		url = TestPyasp.ANY_URL
		self.pyasp.eventvalidation = TestPyasp.SAMPLE_B64

		self.pyasp.post(TestPyasp.ANY_URL)

		mock_requests.post.assert_called_with(url, headers={'__EVENTVALIDATION': TestPyasp.SAMPLE_B64})

	@responses.activate
	def test_viewstates_are_cleared_after_each_request(self):
		"""Are captured __VIEWSTATE fields cleared
		after each request?"""
		responses.add(
			responses.GET, TestPyasp.ANY_URL,
			body='<html><body><input type="hidden" name="__VIEWSTATE" value="{}"/>' \
				'<input type="hidden" name="__EVENTVALIDATION" value="{}"/></body></html>'
					.format(TestPyasp.SAMPLE_B64, TestPyasp.SAMPLE_B64_2))

		responses.add(
			responses.GET, TestPyasp.ANY_URL_2,
			body='<html><body><input type="hidden" name="__VIEWSTATE" value="{}"/></body></html>'.format(TestPyasp.SAMPLE_B64_2))

		self.pyasp.get(TestPyasp.ANY_URL)
		self.pyasp.get(TestPyasp.ANY_URL_2)

		assert len(self.pyasp.viewstates) == 1
		assert self.pyasp.eventvalidation is None

	@mock.patch('pyasp.pyasp.requests')
	def test_get_with_custom_headers(self, mock_requests):
		"""Are custom headers sent when issuing
		GET requests?"""
		url = TestPyasp.ANY_URL
		custom_headers = {'X-My-Get-Header': 'value'}

		self.pyasp.get(url, custom_headers)

		mock_requests.get.assert_called_with(url, headers=custom_headers)

	@mock.patch('pyasp.pyasp.requests')
	def test_post_with_custom_headers(self, mock_requests):
		"""Are custom headers sent when issuing
		POST requests?"""
		url = TestPyasp.ANY_URL_2
		custom_headers = {'X-My-Post-Header': 'value'}

		self.pyasp.post(url, custom_headers)

		mock_requests.post.assert_called_with(url, headers=custom_headers)

	@mock.patch('pyasp.pyasp.requests')
	def test_put_with_custom_headers(self, mock_requests):
		"""Are custom headers sent when issuing
		PUT requests?"""
		url = TestPyasp.ANY_URL
		custom_headers = {'X-My-Put-Header': 'value'}

		self.pyasp.put(url, custom_headers)

		mock_requests.put.assert_called_with(url, headers=custom_headers)