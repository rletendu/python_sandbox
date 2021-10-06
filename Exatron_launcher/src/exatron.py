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

class ExatronState(Enum):
    OFFLINE = 1
    CONNECTED = 2
    READY = 3
    WORKING = 4

class ExaComTCP(threading.Thread):
    def __init__(self, host, port, demo=False) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo =demo
        self.state = ExatronState.OFFLINE
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(1)
        self.log.info("TCP Server listening on {}:{}".format(host, port))
        self.alive = True
        self.eolFlag = False

    def run(self) -> None:
        while True and self.alive:
            if self.state == ExatronState.OFFLINE:
                (self.conn, self.addr) = self.server.accept()
                self.state = ExatronState.CONNECTED
                self.log.info("TCP connection with {}".format(self.addr[0]))
            elif self.state == ExatronState.CONNECTED:
                self.conn.settimeout(2)
                try:
                    r = self.get()
                    if r =="H\r":
                        self.state = ExatronState.READY
                        self.conn.settimeout(3600)
                except socket.timeout:
                    pass
            elif self.state == ExatronState.READY:
                if self.eolFlag:
                    self.eolFlag = False
                    self.state = ExatronState.CONNECTED
                    self.log.info("EOL Flag received, back to ready detection state")

    def send(self, data):
        if self.state != ExatronState.OFFLINE:
            self.log.info("Sending {}".format(data))
            self.conn.send(data.encode())

    def get(self):
        if self.state != ExatronState.OFFLINE:
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
        if self.state != ExatronState.OFFLINE:
            self.conn.settimeout(timeout)

    def close(self):
        self.alive = False

    def __del__(self):
        self.alive = False
        self.conn.close()
        self.server.close()


class ExaComSerial(threading.Thread):
    def __init__(self, port, baud=115200, demo=False) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo = demo
        self.port = port
        self.baud = baud
        self.state = ExatronState.OFFLINE
        if not self.demo:
            self.ser = serial.Serial(port, baudrate=baud, timeout=3)
        self.alive = True
        self.eolFlag = False

    def run(self) -> None:
        self.state = ExatronState.CONNECTED
        while True and self.alive:
            if self.state == ExatronState.OFFLINE:
                (self.conn, self.addr) = self.server.accept()
                self.state = ExatronState.READY
                self.log.info("TCP connection with {}".format(self.addr[0]))
            elif self.state == ExatronState.CONNECTED:
                r = self.get()
                if r =="H\r":
                    self.state = ExatronState.READY
            elif self.state == ExatronState.READY:
                if self.eolFlag:
                    self.eolFlag = False
                    self.state = ExatronState.CONNECTED

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

        if com_port is not None and tcp_port is None:
            self.ExaCom = ExaComSerial(port=com_port, demo=demo)
        elif com_port is None and tcp_port is not None:
            local_ip = socket.gethostbyname(socket.gethostname())
            self.ExaCom = ExaComTCP(port=tcp_port,host=local_ip, demo=demo)
            self.ExaCom.start()
        else:
            raise "Invalid Exatron Interface"

    def get_state(self):
        return self.ExaCom.state

    def get_temperature(self):
        if self.demo:
            return self.temperature
        self.ExaCom.send("GET_TEMP?")
        r = self.ExaCom.get()
        try:
            t = float(r.replace("CUR_TEMP,","").replace("\r",''))
        except Exception as e:
            print("Error reading temp: {}".format(e))
            t= 255
            pass
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

    def set_temperature(self, temp, shiller=None, accuracy=None, soak=None):
        if shiller is None:
            if temp < 20:
                shiller = "COLD"
            elif temp == 25:
                shiller = "ROOM"
            elif temp > 25:
                shiller = "HOT"
        if accuracy is None:
            low_band = self.low_band
            high_band = self.high_band
        else:
            low_band = accuracy
            high_band = accuracy
        if soak is None:
            soak = self.soak


        if self.demo:
            self.log.info("Seting temp {} shiller {}".format(temp,shiller))
            self.temperature = temp
            return True
        self.ExaCom.send("SET_TEMP,{:.01f},UPPER_BAND,{},LOWER_BAND,{},{},SOAK_TIME,{}".format(temp,high_band,low_band,shiller,soak))
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
        self.ExaCom.eolFlag = True
        return True

    def close(self):
        self.ExaCom.close()
        self.ExaCom.__del__()


