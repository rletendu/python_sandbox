import argparse
import os
import shutil
import socket
import threading
import serial
import serial.tools.list_ports
import time
from netifaces import interfaces, ifaddresses, AF_INET
import queue
import logging
import sys

NB_GET_TEMP_BEFORE_OK = 1

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    parser.add_argument('--demo', action='store_true',
                        help='Activate Demo mode')
    parser.add_argument('--com_port', default=None,
                        help='Serial com port')
    parser.add_argument('--tcp_port', default=4000,
                        help='TCP IP server port number')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
    log = logging.getLogger(__name__)

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.info("Starting")
    else:
        log.setLevel(logging.CRITICAL)

    print("Machine Local IP:")
    local_ip = socket.gethostbyname(socket.gethostname())
    print(local_ip)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((local_ip, args.tcp_port))

    try:
        while True:
            input("press any key for handler ready:")
            s.sendall("H\r".encode())
            temp = 25.0
            target_temp = temp
            cnt = NB_GET_TEMP_BEFORE_OK
            while(True):
                rx = s.recv(1024).decode()
                print(rx)
                if rx=="GET_TEMP?":
                    cnt +=1
                    if cnt>=NB_GET_TEMP_BEFORE_OK:
                        real_temp=target_temp
                    else:
                        real_temp=target_temp-10
                    s.sendall("CUR_TEMP,{}\r".format(real_temp).encode())
                elif rx=="R":
                    s.sendall("S\r".format(temp).encode())
                elif rx=="TEST_RESULT,1":
                    s.sendall("H\r".format(temp).encode())
                elif rx=="R":
                    s.sendall("S\r".format(temp).encode())
                elif rx.startswith("SET_TEMP"):
                    t = rx.split(",")
                    target_temp = float(t[1])
                    print("Target temp : {}".format(target_temp))
                    cnt = 0
                    s.sendall("OK\r".format(temp).encode())
                elif rx=="EOL":
                    break
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            s.close
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    s.close()