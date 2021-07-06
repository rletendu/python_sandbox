#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe, sys, os
import update_version
import stat
import revision
from time import sleep
import argparse
from subprocess import call
from shutil import copy
from site import getsitepackages
import shutil


RELEASE_FOLDER = "release"
MAIN_SCRIPT_FILES = ("arb_src_generator.py", )
DESCRIPTION ="Automated Regression Bench"


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
	parser.add_argument('--tool', default='py2exe')
	parser.add_argument('--makespec', action='store_true')
	args = parser.parse_args()

	if args.makespec:
		call(["pyi-makespec","--onefile","--windowed", MAIN_SCRIPT_FILE])
		sys.exit(0)

	if not os.path.exists(RELEASE_FOLDER):
		os.makedirs(RELEASE_FOLDER)
	else:
		remove_read_only(RELEASE_FOLDER)
		shutil.rmtree(RELEASE_FOLDER)
		os.makedirs(RELEASE_FOLDER)

	build_number = update_version.inc_build_version("revision.py")
	print("Updated Build number:",build_number)
	rev = revision.REVISION + '.'+ str(build_number)
	print("Building New Version: ", rev)

	site_packages = getsitepackages()
	for p in site_packages:
		if 'site-packages' in p:
			site_package_path = p
			break;
	print("Using Site package folder:",site_package_path)


	if args.tool == 'py2exe':
		import py2exe
		sys.argv.insert(1, 'py2exe')
		sys.argv = sys.argv[0:2]
		for script in MAIN_SCRIPT_FILES:
			print("## Building using py2exe for {}".format(script))
			setup(
				name= os.path.splitext(script)[0],
				version=revision.REVISION + '.'+ str(revision.BUILD),
				description=DESCRIPTION,
				author="rletendu",
				console = [{
					'script': script}],
				data_files = [
					],
				options = {'py2exe': {
					'bundle_files': 3, # 3: Nobundle(Needed by openpyxl) 1:Bundle AlL
					"unbuffered": True,
					'compressed': False,
					'packages': [],
					'includes': [],
					'excludes': ['tkinter', 'matplotlib', 'numpy', 'zmq', 'IPython', 'sympy', 'win32com', 'pywintypes'],
					'dist_dir':RELEASE_FOLDER }},
				zipfile = None
			)
			print("Done building with py2exe for {}".format(script))

	elif args.tool == 'cx_freeze':

		from cx_Freeze import setup, Executable
		sys.argv.insert(1,'build')
		sys.argv = sys.argv[0:2]
		for script in MAIN_SCRIPT_FILES:
			print("## Building using Cx_Freeze")
			build_exe_options = {
				"packages": ["os",'instruments_drivers','packaging' ],
				'excludes':['tkinter', 'matplotlib', 'numpy', 'zmq', 'IPython'],
				'includes':['sip', 'appdirs'],
				"build_exe":RELEASE_FOLDER,
				#'compressed': True,
			}

			# GUI applications require a different base on Windows (the default is for a
			# console application).
			base = None
			if sys.platform == "win32":
				#base = "Win32GUI"
				pass

			setup(  name= os.path.splitext(script)[0],
				version=revision.REVISION + '.'+ str(revision.BUILD),
				description=DESCRIPTION,
				author="rletendu",
				options = {"build_exe": build_exe_options},
				data_files = [

					],
				windows = [{
					'script': script,
					"icon_resources": [(0, "icon.ico")]}],
				zipfile = True,
				executables = [Executable(script, base=base)]),

	elif args.tool == 'pyinstaller':
		print("## Building using pyinstaller")
		# call(["pyinstaller","--onefile","--windowed", "powerbench_gui.spec", "--distpath",RELEASE_FOLDER])
		call(["pyinstaller","--windowed", os.path.splitext(MAIN_SCRIPT_FILE)[0]+".spec", "--distpath",RELEASE_FOLDER ])

	print("Built New Version: ", rev)
	sleep(1)

