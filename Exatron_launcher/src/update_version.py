#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

def inc_build_version(version_file):
	with open(version_file,'r') as f:
	    lines = f.readlines()

	with open(version_file,'w') as f:
		for line in lines :
			if "BUILD =" in line:
				s=line.replace(" ","")
				s=s[1+s.find("="):]
				build=eval(s)+1
				line="BUILD = {}\n".format(str(build))
			elif "BUILD_DATE =" in line:
				line = "BUILD_DATE = '{}'\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			f.write(line)
	return build

if __name__ == '__main__':
	inc_build_version('revision.py')