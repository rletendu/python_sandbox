import logging
import threading
import serial
import serial.tools.list_ports
import time
from .exatronstate import ExatronState

class ExaComSerial(threading.Thread):
    def __init__(self, port, baud=115200, demo=False, asynch=True) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo = demo
        self.port = port
        self.baud = baud
        self.asynch = asynch
        self.state = ExatronState.OFFLINE
        self.ser = None
        if not self.demo:
            self.ser = serial.Serial(port, baudrate=baud, timeout=None)

        if self.asynch:    
            self.alive = True
        else:
            self.alive = False
        self.cnt = 0

    def run(self) -> None:
        if self.demo:
            while self.alive:
                if self.state == ExatronState.OFFLINE:
                    time.sleep(2)
                    self.state = ExatronState.READY
                elif self.state == ExatronState.CONNECTED:
                    time.sleep(5)
                    self.state = ExatronState.READY
                elif self.state == ExatronState.READY:
                    pass
        else:
            while self.alive:
                if self.state == ExatronState.OFFLINE:
                    self.state = ExatronState.READY
                elif self.state == ExatronState.CONNECTED:
                    if self.demo:
                        time.sleep(5)
                        self.state = ExatronState.READY
                    else:
                        r = self.get()
                        if r =="H\r":
                            self.state = ExatronState.READY
                elif self.state == ExatronState.READY:
                    pass


    def waitConnected(self):
        if self.demo:
            time.sleep(2)
            if not self.asynch:
                self.state = ExatronState.CONNECTED
            return
        if self.asynch:
            while self.state != ExatronState.CONNECTED:
                pass
            return True
        else:
            if self.state == ExatronState.OFFLINE:
                self.state = ExatronState.CONNECTED
            return True

    def waitReady(self, timeout=None):
        if self.demo:
            time.sleep(2)
            if not self.asynch:
                self.state = ExatronState.READY
            return
        if self.asynch:
            while self.state != ExatronState.READY:
                pass
            return True
        else:
            if timeout:
                self.setTimeout(timeout)
            r = self.get()
            if r == "H\r":
                self.state = ExatronState.READY
                self.conn.settimeout(3600)
                return True
            else:
                self.conn.settimeout(3600)
                return False

    def send(self, data, eol=False):
        data = "{}\r".format(data)
        self.log.info("Sending {}".format(data))
        if eol:
            self.state = ExatronState.CONNECTED
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
        if self.ser:
            self.ser.close()
            self.ser = serial.Serial(self.port, baudrate=self.baud, timeout=timeout)

    def close(self):
        self.alive = False
        if self.demo:
            return
        self.ser.close()

    def __del__(self):
        if self.demo:
            return
        if self.ser:
            self.ser.close()