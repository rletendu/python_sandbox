#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import sys, os
import update_version
import stat
import revision
import argparse

from shutil import copy
import PyInstaller.__main__


MAIN_SCRIPT_FILE = "exa_launch.py"
RELEASE_FOLDER_NAME = "../release"

def remove_read_only(path):
	os.chmod( path, stat.S_IWRITE )
	l = os.listdir(path)
	for file in l:
		f = os.path.join(path,file)
		os.chmod( f, stat.S_IWRITE )
		if os.path.isdir(f):
			remove_read_only(f)



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--no_build_inc', action='store_true')
	parser.add_argument('--only_full_license', action='store_true')
	args = parser.parse_args()

	if not args.no_build_inc:
		build_number = update_version.inc_build_version("revision.py")
		print("Updated Build number:",build_number)
		rev = revision.REVISION + '.'+ str(build_number)
		print("Building New Version: ", rev)
	
	dest_folder = os.path.join(RELEASE_FOLDER_NAME)
	print("Creating release folder",dest_folder)
	os.makedirs(dest_folder, exist_ok=True)
	remove_read_only(dest_folder)
	PyInstaller.__main__.run(["-windowed", "exa_launch.spec", "--distpath",dest_folder ])


