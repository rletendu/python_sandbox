import csv
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

	with open('eggs.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
		spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])