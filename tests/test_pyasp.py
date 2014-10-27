import os
import pytest
import unittest

from pyasp.pyasp import Pyasp

class TestPyasp(unittest.TestCase):
	def setup_method(self, method):
		"""Does the library use the default cookie
		jar file if none is specified?"""
		self.pyasp = Pyasp()
		assert self.pyasp.cookiejar == Pyasp.DEFAULT_COOKIEJAR

	def test_default_cookie_jar(self):
		"""Does the library use the specified cookie
		jar file if one is provided?"""
		self.pyasp = Pyasp(cookiejar="/tmp/custom.jar")
		assert self.pyasp.cookiejar == "/tmp/custom.jar"