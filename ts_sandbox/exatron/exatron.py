import logging
import socket
from enum import Enum
import sys
from .exacomserial import ExaComSerial
from .exacomtcp import ExaComTCP



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

