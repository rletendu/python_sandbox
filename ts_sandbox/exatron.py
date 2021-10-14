import logging
import socket
import threading
import serial
import serial.tools.list_ports
import time
from enum import Enum
import sys

class ExatronState(Enum):
    OFFLINE = 1
    CONNECTED = 2
    READY = 3
    WORKING = 4

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


class ExaComSerial(threading.Thread):
    def __init__(self, port, baud=115200, demo=False, asynch=True) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.demo = demo
        self.port = port
        self.baud = baud
        self.asynch = asynch
        if self.asynch:
            self.state = ExatronState.OFFLINE
            self.alive = True
        else:
            self.alive = False
        if not self.demo:
            self.ser = serial.Serial(port, baudrate=baud, timeout=None)
        self.cnt = 0

    def run(self) -> None:
        while True and self.alive:
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
        if self.asynch:
            while self.state == ExatronState.CONNECTED:
                pass
            return True
        else:
            if self.state == ExatronState.OFFLINE:
                self.state = ExatronState.CONNECTED
            return True

    def waitReady(self, timeout=None):
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
        self.ser.close()

class ExaTron(object):
    def __init__(self, com_port=None, tcp_port=None, demo=False, accuracy=2.0, soak=4, asynch=True):
        self.log = logging.getLogger()
        self.demo = demo
        self.soak = soak
        self.low_band = accuracy
        self.high_band = accuracy
        self.temperature = 25
        if com_port == False:
            com_port = None

        if tcp_port == False:
            tcp_port = None

        if com_port is not None and tcp_port is None:
            self.ExaCom = ExaComSerial(port=com_port, demo=demo, asynch=asynch)
            if asynch:
                self.ExaCom.start()
        elif com_port is None and tcp_port is not None:
            local_ip = socket.gethostbyname(socket.gethostname())

            self.log.info('Local Ip : {}'.format(local_ip))
            self.ExaCom = ExaComTCP(port=tcp_port,host=local_ip, demo=demo, asynch=asynch)
            if asynch:
                self.ExaCom.start()
        else:
            raise "Invalid Exatron Interface"

    def waitConnected(self):
        return self.ExaCom.waitConnected()

    def waitReady(self):
        return self.ExaCom.waitReady()

    def get_state(self):
        return self.ExaCom.state

    def get_name_state(self):
        return self.ExaCom.state.name

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
        if self.demo:
            self.log.info("Sending EOL")
            return True
        self.ExaCom.send("EOL",eol=True)
        return True

    def close(self):
        self.ExaCom.close()
        self.ExaCom.__del__()

if __name__ == '__main__':
    def exa_tester(exatron):
        print("Waiting Handler connection ....")
        exatron.waitConnected()
        print("Connected")
        for j in range(2):
            print("Waiting Handler ready ....")
            exatron.waitReady()
            print("Ready")
            for i in range(10):
                print("Loading part ....")
                exatron.load_next_part()
                for temp in (85,25,125):
                    print("Setting temp : {}".format(temp))
                    exatron.set_temperature(temp)
                print("Unloading part ...")
                exatron.unload_part(1)
            print("End of Lot ...")
            exatron.end_of_lot()
        print("All Done")
        exatron.close()

    debug_level = logging.DEBUG
    FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'
    logging.basicConfig(level=debug_level, format=FORMAT, stream=sys.stderr)
    log = logging.getLogger(__name__)
    exatron = ExaTron(com_port=False, tcp_port=4000, demo=False, accuracy=3, soak=10, asynch=False)
    exa_tester(exatron)
    exatron = ExaTron(com_port=False, tcp_port=4000, demo=True, accuracy=3, soak=10, asynch=False)
    exa_tester(exatron)

