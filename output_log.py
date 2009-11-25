""" Output Log - Output entries to a simple log file """
import logging
from flexget.plugin import *

log = logging.getLogger('log')

class OutputLog:

    def validator(self):
	pass

    def get_config(self, feed):
	pass

    def feed_exit(self, feed):
	pass
