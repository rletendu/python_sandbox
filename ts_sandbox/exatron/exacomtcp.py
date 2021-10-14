import logging
import socket
import threading
import time
from .exatronstate import ExatronState

class ExaComTCP(threading.Thread):
    def __init__(self, host, port, demo=False, asynch=True) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo = demo
        self.asynch = asynch
        self.state = ExatronState.OFFLINE
        self.server = None
        self.conn = None
        self.addr = None
        if not self.demo:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((host, int(port)))
            self.server.listen(1)
            self.log.info("TCP Server listening on {}:{}".format(host, port))

        if self.asynch:
            self.alive = True
        else:
            self.alive = False


    def run(self) -> None:
        self.alive = True
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
        else :
            while self.alive:
                if self.state == ExatronState.OFFLINE:
                    (self.conn, self.addr) = self.server.accept()
                    if self.conn:
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
            (self.conn, self.addr) = self.server.accept()
            if self.conn:
                self.state = ExatronState.CONNECTED

    def waitReady(self, timeout=None):
        if self.demo:
            time.sleep(2)
            if not self.asynch:
                self.state = ExatronState.CONNECTED
            return
        if self.asynch:
            while self.state != ExatronState.READY:
                pass
            return True
        else:
            if timeout:
                self.conn.settimeout(timeout)
            r = self.get()
            if r == "H\r":
                self.state = ExatronState.READY
                self.conn.settimeout(3600)
                return True
            else:
                self.conn.settimeout(3600)
                return False

    def send(self, data, eol=False):
        if self.state != ExatronState.OFFLINE:
            self.log.info("Sending {}".format(data))
            self.conn.send(data.encode())
            if eol:
                self.state = ExatronState.CONNECTED


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
        if self.conn:
            self.conn.close()
        if self.server:
            self.server.close()
