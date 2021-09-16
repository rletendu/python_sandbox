import logging
import argparse
import os
import shutil
import socket
import threading
import serial
import serial.tools.list_ports
import time


LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

"""
"R"
"EOL"
"GET_TEMP?"
"SET_TEMP,85.0,UPPER_BAND,200,LOWER_BAND,200,HOT,SOAK_TIME,3"
"SET_TEMP,-40.0,UPPER_BAND,200,LOWER_BAND,200,COLD,SOAK_TIME,4"
"SET_TEMP,25.0,UPPER_BAND,200,LOWER_BAND,200,ROOM,SOAK_TIME,1"
"TEST_RESULT,1"
"""

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
        self.log.info("Sending {}".format(data))
        self.conn.send(data)

    def get(self):
        data = self.conn.recv(1024)
        self.log.info("Received {}".format(data))
        return data

    def __del__(self):
        self.TcpSoocket.close()


class ExaComSerial(object):
    def __init__(self, port) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.ser = serial.Serial(port, baudrate=9600, timeout=3)

    def send(self, data):
        self.log.info("Sending {}".format(data))
        self.ser.write(data)

    def get(self):
        data = self.ser.readline().decode()
        self.log.info("Received {}".format(data))
        return data

class Exa(object):
    def __init__(self, com_port=None, tcp_port=None):
        if com_port is not None and tcp_port is None:
            self.ExaCom = ExaComSerial(port=com_port)
        elif com_port is None and tcp_port is not None:
            self.ExaCom = ExaComTCP(port=tcp_port)
        else:
            raise "Invalid Exatron Interface"

    def wait_ready(self):
        r = self.ExaCom.get()
        if r =="H\r":
            return True
        else:
            return False

    def get_temperature(self):
        self.ExaCom.send("GET_TEMP?\r")
        r = self.ExaCom.get()
        t = float(r.replace("CUR_TEMP,","").replace("\r"))
        return t

    def load_next_part(self):
        self.ExaCom.send("R\r")
        r = self.ExaCom.get()
        if r =="OK\r":
            return True
        else:
            return False
        
    def unload_part(self, bin=1):
        self.ExaCom.send("TEST_RESULT,{}\r".format(bin))
        r = self.ExaCom.get()
        if r =="OK\r":
            return True
        else:
            return False

    def set_temperature(self, temp):
        if temp < 20:
            shiller = "COLD"
        elif temp == 25:
            shiller = "ROOM"
        elif temp > 25:
            shiller = "HOT"
        self.ExaCom.send("SET_TEMP,{},UPPER_BAND,200,LOWER_BAND,200,{},SOAK_TIME,4".format(temp,shiller))
        r = self.ExaCom.get()
        if r =="OK\r":
            return True
        else:
            return False
    
    def end_of_lot(self):
        self.ExaCom.send("EOL\r")
        r = self.ExaCom.get()
        if r =="OK\r":
            return True
        else:
            return False

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


	com_list = serial.tools.list_ports.comports()
    for com in com_list:
        log.info(com)
        if args.com is None:
            args.com = com.device
            print("No COM port specified using {}".format(args.com))
            break

    exatron = Exa(com_port=)
    exatron.wait_ready()
    for i in range(5):
        exatron.set_temperature(25)
        exatron.load_next_part()
        time.sleep(10)
        exatron.unload_part()

    
