import logging
import argparse
import subprocess
import os
import shutil

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

REPOS = [
    {'name': 'instr.lib', 'url': "ssh://git@bitbucket.microchip.com/sof/instr.lib.git",
        'dst': "C:\\Program Files\\National Instruments\\LabVIEW 2019\\instr.lib"},
    {'name': 'user.lib', 'url': "ssh://git@bitbucket.microchip.com/sof/user.lib.git",
        'dst': "C:\\Program Files\\National Instruments\\LabVIEW 2019\\user.lib"},
    {'name': 'Components', 'url': "ssh://bitbucket.microchip.com/scm/sof/components.git",
        'dst': "C:\\Users\Public\\Documents\\National Instruments\\TestStand 2019 (64-bit)\\Components"},
    {'name': 'System', 'url': "ssh://bitbucket.microchip.com/scm/sof/mchp.lvlib.git",
        'dst': "C:\\Users\Public\\Documents\\National Instruments\\TestStand 2019 (64-bit)\\Applications\\Microchip\\System"}
]

def confirm(msg):
    r = input("{} (Y)/n :".format(msg))
    if r=="" or r=="Y" or r=='y':
        return True
    else:
        return False

    
def empty_folder(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            os.unlink(os.path.join(root, name))
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))


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

    for repo in REPOS:
        print("Cloning {} from {} into {}".format(
            repo["name"], repo["url"], repo["dst"]))

        if confirm('Empty {} folder ?'.format(repo["dst"])):
            empty_folder(repo["dst"])
        else:
            pass
        subprocess.call(['git', 'clone', repo["url"], repo["dst"]])
