#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, shutil, os
import logging
import argparse
from bs4 import BeautifulSoup, Tag, CData

if __name__ == '__main__':
	soup = BeautifulSoup('<!DOCTYPE html>', 'html.parser')
	html = Tag(soup, name='html')
	soup.append(html)
	body = Tag(soup, name='body')
	body.string = "Hello !"
	html.insert(0,body)
	print(soup.prettify("utf-8"))
	with open("index.html", "w") as file:
		file.write(str(soup))
	
	
	