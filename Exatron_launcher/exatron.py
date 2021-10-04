import logging
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
from enum import Enum



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



class ExaComTCP(threading.Thread):
    def __init__(self, host=HOST, port=DEFAULT_PORT, demo=False) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo =demo
        if demo:
            self.connected = True
            self.ready = True
        else:
            self.connected = False
            self.ready = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(1)
        self.log.info("TCP Server listening on {}:{}".format(host, port))

    def run(self) -> None:
        (self.conn, self.addr) = self.server.accept()
        self.connected = True
        self.log.info("TCP connection with {}".format(self.addr[0]))
        while True and self.connected:
            while self.ready:
                pass
            r = self.get()
            if r =="H\r":
                self.ready = True

    def is_connected(self):
        return self.connected

    def is_ready(self):
        return self.ready

    def clear_ready(self):
        self.ready = False

    def send(self, data):
        if self.is_connected:
            self.log.info("Sending {}".format(data))
            self.conn.send(data.encode())

    def get(self):
        if self.is_connected:
            if self.demo:
                return
            try:
                data = self.conn.recv(1024)
                self.log.info("Received {}".format(data))
                return data.decode()
            except socket.timeout: 
                self.log.info("No answer from client (timeout)")
                return ""
        else:
            return ""

    def setTimeout(self, timeout):
        if self.is_connected():
            self.conn.settimeout(timeout)

    def close(self):
        self.is_connected = False

    def __del__(self):
        self.conn.close()
        self.server.close()


class ExaComSerial(object):
    def __init__(self, port, baud=115200, demo=False) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo = demo
        self.port = port
        self.baud = baud
        if demo:
            self.connected = True
            self.ready = True
            return
        else:
            self.connected = True #For Serial connection is available right now
            self.ready = False
        self.ser = serial.Serial(port, baudrate=baud, timeout=3)

    def is_ready(self):
        return self.ready

    def is_connected(self):
        return self.connected

    def send(self, data):
        data = "{}\r".format(data)
        self.log.info("Sending {}".format(data))
        if self.demo:
            return
        self.ser.write(data.encode())

    def get(self):
        if self.demo:
            return
        data = self.ser.readline().decode()
        self.log.info("Received {}".format(data))
        return data

    def setTimeout(self, timeout):
        if self.is_connected():
            self.ser.close()
            self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=timeout)

    def close(self):
        self.ser.close()

    def __del__(self):
        if self.demo:
            return
        self.ser.close()

class ExaTron(object):
    def __init__(self, com_port=None, tcp_port=None, demo=False, accuracy=2.0, soak=4):
        self.log = logging.getLogger()
        self.demo = demo
        self.soak = soak
        self.low_band = accuracy
        self.high_band = accuracy
        self.temperature = 25
        self.ready = False

        if com_port is not None and tcp_port is None:
            self.ExaCom = ExaComSerial(port=com_port, demo=demo)
        elif com_port is None and tcp_port is not None:
            local_ip = socket.gethostbyname(socket.gethostname())
            self.ExaCom = ExaComTCP(port=tcp_port,host=local_ip, demo=demo)
            self.ExaCom.start()
        else:
            raise "Invalid Exatron Interface"

    def is_connected(self):
        return self.ExaCom.is_connected()

    def wait_ready(self, timeout=None):
        if self.demo:
            time.sleep(1)
            return True
        if timeout is not None:
            self.Exacom.SetTimeout(timeout)
        r = self.ExaCom.get()
        if r =="H\r":
            self.ready = True
            return True
        else:
            self.ready = False
            return False

    def is_ready(self):
        return self.ExaCom.is_ready()

    def get_temperature(self):
        if self.demo:
            return self.temperature
        self.ExaCom.send("GET_TEMP?")
        r = self.ExaCom.get()
        t = float(r.replace("CUR_TEMP,","").replace("\r",''))
        return t

    def load_next_part(self):
        if self.demo:
            self.log.info("Loading next part")
            return True
        self.ExaCom.send("R")
        r = self.ExaCom.get()
        if r =="S\r":
            return True
        else:
            return False

    def unload_part(self, bin=1):
        self.log.info("Unloading part with bin {}".format(bin))
        if self.demo:
            return True
        self.ExaCom.send("TEST_RESULT,{}".format(bin))
        r = self.ExaCom.get()
        if r =="H\r":
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

        if self.demo:
            self.log.info("Seting temp {} shiller {}".format(temp,shiller))
            self.temperature = temp
            return True
        self.ExaCom.send("SET_TEMP,{:.01f},UPPER_BAND,200,LOWER_BAND,200,{},SOAK_TIME,{}".format(temp,shiller, self.soak))
        r = self.ExaCom.get()
        if r =="OK\r":
            return True
        else:
            return False
    
    def end_of_lot(self):
        self.ready = False
        if self.demo:
            self.log.info("Sending EOL")
            return True
        self.ExaCom.send("EOL")

        self.log.info("No answer to EOL in TCP/MODE!")
        self.ExaCom.clear_ready()
        return True

    def close(self):
        self.ExaCom.close()
        self.ExaCom.__del__()


