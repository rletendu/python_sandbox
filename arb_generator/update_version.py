#!/usr/bin/env python
# -*- coding: utf-8 -*-

def inc_build_version(version_file):
	with open(version_file,'r') as f:
	    lines = f.readlines()
	    
	with open(version_file,'w') as f:
		for line in lines :
			if "BUILD" in line:
				s=line.replace(" ","")
				s=s[1+s.find("="):]
				build=eval(s)+1
				line="BUILD = "+str(build)
			f.write(line)
	return build