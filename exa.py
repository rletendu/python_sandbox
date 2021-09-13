import logging
import argparse
import os
import shutil
import socket
import threading
import serial


LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'



HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
DEFAULT_PORT = 65432        # P

class ExaComTCP(object):
    def __init__(self, port=DEFAULT_PORT) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.TcpSoocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.TcpSoocket.bind((HOST, port))
        self.conn, self.addr = self.TcpSoocket.accept()

    def send(self, data):
        self.conn.send(data)

    def get(self):
        data = self.conn.recv(1024)
        return data


class ExaComSerial(object):
    def __init__(self, port) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.ser = serial.Serial(port, baudrate=9600, timeout=3)


    def send(self, data):
        self.ser.write(data)

    def get(self):
        data = self.ser.readline().decode()
        return data



class Exa(object):
    def __init__(self):
        self.ExaCom = None

    def wait_ready(self):
        pass

    



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

    
