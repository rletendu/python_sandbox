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
    def __init__(self, host=HOST, port=DEFAULT_PORT) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.connected = False
        self.ready = False
        self.q = queue.Queue()
        #self.server = socket.socket(socket.AF_INET, socket.SOCK_RAW)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(1)
        self.log.info("TCP Server listening on {}:{}".format(host, port))
        #(self.conn, self.addr) = self.server.accept()
        #self.log.info("TCP connection with {}".format(self.addr[0]))

    def run(self) -> None:
        (self.conn, self.addr) = self.server.accept()
        self.connected = True
        r = self.get()
        if r =="H\r":
            self.ready = True
        #self.conn.settimeout()
        self.log.info("TCP connection with {}".format(self.addr[0]))

    def is_connected(self):
        return self.connected

    def is_ready(self):
        return self.ready

    def send(self, data):
        if self.is_connected:
            self.log.info("Sending {}".format(data))
            self.conn.send(data.encode())

    def get(self):
        if self.is_connected:
            try:
                data = self.conn.recv(1024)
                self.log.info("Received {}".format(data))
                return data.decode()
            except socket.timeout: 
                self.log.info("No answer from client (timeout)")
                return ""
        else:
            return ""

    def __del__(self):
        self.conn.close()
        self.server.close()


class ExaComSerial(object):
    def __init__(self, port, baud=115200) -> None:
        super().__init__()
        self.log = logging.getLogger()
        self.ser = serial.Serial(port, baudrate=baud, timeout=3)

    def send(self, data):
        data = "{}\r".format(data)
        self.log.info("Sending {}".format(data))
        self.ser.write(data.encode())

    def get(self):
        data = self.ser.readline().decode()
        self.log.info("Received {}".format(data))
        return data

    def __del__(self):
        self.ser.close()

class Exa(object):
    def __init__(self, com_port=None, tcp_port=None, demo=False, accuracy=2.0, soak=4):
        self.log = logging.getLogger()
        self.demo = demo
        self.soak = soak
        self.low_band = accuracy
        self.high_band = accuracy
        self.temperature = 25
        self.ready = False
        if self.demo:
            return
        if com_port is not None and tcp_port is None:
            self.ExaCom = ExaComSerial(port=com_port)
        elif com_port is None and tcp_port is not None:
            local_ip = socket.gethostbyname(socket.gethostname())
            self.ExaCom = ExaComTCP(port=tcp_port,host=local_ip)
            self.ExaCom.start()
        else:
            raise "Invalid Exatron Interface"


    def wait_ready(self):
        if self.demo:
            time.sleep(1)
            return True
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
        #'INPUT_TRAY,1,ROW,1,COL,1\r'
        if r =="OK\r":
            return True
        else:
            return False
        
    def unload_part(self, bin=1):
        self.log.info("Unloading part with bin {}".format(bin))
        if self.demo:
            return True
        self.ExaCom.send("TEST_RESULT,{}".format(bin))
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
        r = self.ExaCom.get()
        if r =="OK\r":
            return True
        else:
            return False

    def close(self):
        self.ExaCom.__del__()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    parser.add_argument('--demo', action='store_true',
                        help='Activate Demo mode')
    parser.add_argument('--com_port', default=None,
                        help='Serial com port')
    parser.add_argument('--tcp_port', action=None,
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

#    for ifaceName in interfaces():
#        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
#        print(' '.join(addresses))

    
    com_list = serial.tools.list_ports.comports()
    if len(com_list)==0:
        print("No COM port available on this machine")
    for com in com_list:
        log.info(com)
        if args.com_port is None:
            args.com_port = com.device
            print("No COM port specified using {}".format(args.com_port))
            break
    if args.tcp_port is None:
        exatron = Exa(com_port=args.com_port)
    else:
        exatron = Exa(tcp_port=int(args.tcp_port))

    exatron.wait_ready()
    for i in range(5):
        exatron.set_temperature(25)
        time.sleep(1)
        exatron.load_next_part()
        print("Dummy testing time for 5s ...")
        time.sleep(5)
        exatron.unload_part()
        time.sleep(1)
    exatron.end_of_lot()

