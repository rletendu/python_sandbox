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
	parser.add_argument('--baud', action='store_true', default=115200)
	parser.add_argument('--com', default=None)
	args = parser.parse_args()

	logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
	log = logging.getLogger(__name__)
	
	if args.debug:
		log.setLevel(logging.DEBUG)
		log.info("Starting")
	else:
		log.setLevel(logging.CRITICAL)

	com_list = serial.tools.list_ports.comports()
	for com in com_list:
		log.info(com)
		if args.com is None:
			args.com = com.device
			print("No COM port specified using {}".format(args.com))

	ser = serial.Serial(args.com, baudrate=args.baud, timeout=3)

	try:
		while True:
			print(ser.write("U01234567890abcdefghijklmnopqrstU".encode()))
	except KeyboardInterrupt:
		#subprocess.call("cls", shell=True)
		print("Done")