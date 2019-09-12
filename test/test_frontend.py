import unittest
from RIXSPlot.__main__ import main_window
import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)


class Test(unittest.TestCase):
	def setUp(self):
		ex = main_window

	def tearDown(self):
		pass

	def testName(self):
		pass


if __name__ == "__main__":
	# import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
