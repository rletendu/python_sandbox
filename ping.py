import logging
import argparse
#import keyboard
import time
import csv
import subprocess


LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
    log = logging.getLogger(__name__)

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.info("Starting")
    else:
        log.setLevel(logging.CRITICAL)

    with open('addr.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first_line = next(spamreader)
        for row in spamreader:
            try:
                ip = row[1]
                print('Pinging :',ip)
                out = subprocess.check_output(['ping', ip], shell=True)
                print(out.decode())
            except subprocess.CalledProcessError:
                print('Fail to ping {}'.format(ip))