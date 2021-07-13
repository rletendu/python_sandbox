import logging
import argparse
import subprocess
import os
import shutil
from atlassian import Confluence
import getpass

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'

CONFLUENCE_SERVER = "https://confluence.microchip.com"
parent_space = 'HPMDVAL'
children_pages = []

def confirm(msg):
    r = input("{} (Y)/n :".format(msg))
    if r == "" or r == "Y" or r == 'y':
        return True
    else:
        return False


def empty_folder(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            os.unlink(os.path.join(root, name))
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))


def find_subpages(confluence, parent):
    global children_pages
    pages = []
    parent_id = confluence.get_page_id(args.space, parent)
    while True:
        chunk = confluence.get_page_child_by_type(
        parent_id, start=len(pages))
        if len(chunk):
            children_pages += chunk
            pages += chunk
            for p in chunk:
                find_subpages(confluence, p['title'])
        else:
            break
    pass



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Activate Debug mode with verbose execution trace information')
    parser.add_argument('--parent', action='store')
    parser.add_argument('--space', action='store', default='HPMDVAL')
    parser.add_argument('--search_pattern', action='store', default=None)
    parser.add_argument('--replace_pattern', action='store', default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
    log = logging.getLogger(__name__)

    if args.debug:
        log.setLevel(logging.DEBUG)
        log.info("Starting")
    else:
        log.setLevel(logging.CRITICAL)

    user = input("User (you) that will be use to access MCHP Confluence ({} by default) :".format(getpass.getuser()))
    if user == "":
        user = getpass.getuser()
    password = getpass.getpass("Password:")
    confluence = Confluence(url=CONFLUENCE_SERVER, username=user, password=password)
    logging.getLogger('atlassian').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)


    find_subpages(confluence, args.parent)

    for page in children_pages:
        title = page['title']
        if title.find(args.search_pattern) >= 0:
            new_title = title.replace(args.search_pattern, args.replace_pattern)
            print(page['title'],'--->', new_title)
            page['tile'] = new_title
#            confluence.update_page(page['id'], new_title)
        else:
            print("Skipping {} page".format(title))

    
