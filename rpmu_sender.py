import serial
from serial.serialutil import Timeout
import serial.tools.list_ports
import logging
import argparse
import keyboard
import time

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    parser.add_argument('--baud', action='store', default=115200)
    parser.add_argument('--com', action='store', default=None)
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

    ser.dtr = True # DTR = 0 -> RESET = 1
    time.sleep(0.1)
    ser.dtr = False # DTR = 1 -> RESET = 0
    ser.write(
        "AA-FCT:arbtest_sercom_usart_selfloopback-0-0-115200-0-5-0-0-0-0-0-0-0-55\n".encode())
    print(ser.readline().decode(), end="")

    print("Done")
