import serial
from serial.serialutil import Timeout
import serial.tools.list_ports
import logging
import argparse
import subprocess

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', action='store_true', help='Activate Debug mode with verbose execution trace information')
	args = parser.parse_args()

	logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
	log = logging.getLogger(__name__)
	
	if args.debug:
		log.setLevel(logging.DEBUG)
		log.info("Starting")
	else:
		log.setLevel(logging.CRITICAL)

