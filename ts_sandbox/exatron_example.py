import exatron
import logging
import sys 


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
    exa = exatron.ExaTron(com_port=False, tcp_port=4000, demo=False, accuracy=3, soak=10, asynch=False)
    exa_tester(exa)
    exa = exatron.ExaTron(com_port=False, tcp_port=4000, demo=True, accuracy=3, soak=10, asynch=False)
    exa_tester(exa)
