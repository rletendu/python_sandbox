#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import sys
import argparse
import logging
from openpyxl import load_workbook
import os
import revision

# Return a formated string of date+time
def get_timestamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%fct_dict %H:%M:%S')


def parse_excel_sheet(book, sheet_name, parse_by='row', max_item=None):
	if parse_by == 'row':
		book = load_workbook(book, read_only=True)
	else:
		book = load_workbook(book)
	d_list = []
	keys = []
	sheet = book.get_sheet_by_name(sheet_name)
	if parse_by == 'row':
		row_index = 0
		for row in sheet.rows:
			fct_dict = {}
			col_index = 0
			for cell in row:
				if row_index:
					fct_dict[keys[col_index]] = cell.value
				else:
					keys.append(cell.value)
				col_index += 1
			if row_index:
				d_list.append(fct_dict)

			if max_item is not None:
				if row_index >= max_item:
					break;
			row_index += 1
	elif parse_by == 'col':
		col_index = 0
		for col in sheet.columns:
			fct_dict = {}
			row_index = 0
			for cell in col:
				if col_index:
					fct_dict[keys[row_index]] = cell.value
				else:
					keys.append(cell.value)
				row_index += 1
			if col_index:
				d_list.append(fct_dict)
			if max_item is not None:
				if col_index >= max_item:
					break;
			col_index += 1
	return d_list


#
# MAIN top level application entry point
#
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', action='store_true')
	parser.add_argument('--debug_console', action='store_true')
	parser.add_argument('--param_file', action='store', default="arb.xlsm")
	parser.add_argument('--test_sheet', action='store', default="tests")
	parser.add_argument('--test_header_file', action='store', default="arb_test.h")
	parser.add_argument('--arb_decoder_file', action='store', default="arb_decoder.h")
	args = parser.parse_args()

	if args.debug or args.debug_console:
		debug_level = logging.DEBUG
	else:
		debug_level = logging.ERROR
	FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(funcName)s :: %(message)s'
	if args.debug_console:
		logging.basicConfig(level=debug_level, format=FORMAT, stream = sys.stdout)
	else:
		logging.basicConfig(level=debug_level, format=FORMAT)
	log = logging.getLogger(__name__)
	log.info("Starting")

	# Extract parameters
	outfile = open(args.test_header_file,'w')
	test_list = parse_excel_sheet(args.param_file, args.test_sheet)
	log.info("Test_list %s",test_list)
	rev = revision.REVISION + '.'+ str(revision.BUILD)

	outfile.write("//Auto-generated file with arb_src_generator {}\n".format(rev) )
	f_name = os.path.basename(args.test_header_file).upper().replace(".", "_")
	outfile.write("//Automatically  Generated define from config file\n")
	outfile.write("\n#ifndef {}_INCLUDED\n".format(f_name))
	outfile.write("#define {}_INCLUDED\n\n".format(f_name))
	done_list = []
	nb_case = 0
	fct_list = []
	fct_dict = {}
	for test in test_list:
		fct_name = "arbtest"
		fct_prototype = "void "
		for i in range(21):
			if 'test_name' + str(i) in test:
				if test['test_name' + str(i)] is not None and test['test_name' + str(i)] != "":
					fct_name += '_'
					fct_name +=test['test_name' + str(i)].lower()
		if fct_name not in fct_dict:
			fct_dict[fct_name] = {}
			fct_dict[fct_name]['test'] = []
			fct_dict[fct_name]['param_type_list'] = []
		else :
			continue

		param_type_list = []
		fct_list.append(fct_name)
		fct_prototype += fct_name+"("
		for i in range(21):
			if 'dyn_param' + str(i) in test:
				if test['dyn_param' + str(i)] is not None and test['dyn_param' + str(i)] != "":
					if i > 0:
						fct_prototype += ', '
					param_list = test['dyn_param' + str(i)].split(';')
					p_type = param_list[1]
					p_name = param_list[0]
					fct_prototype += p_type
					fct_prototype += ' '
					fct_prototype +=  p_name
					param_type_list.append(p_type)
		fct_prototype += ");"
		fct_dict[fct_name]['param_type_list'] = param_type_list
		if test['comment']:
			comment_list = test['comment'].split('\n')
			for comment in comment_list:
				outfile.write("//{}\n".format(comment))
		outfile.write(fct_prototype)
		outfile.write("\n")
		nb_case += 1
	outfile.write("// Automated Arb_Test Header Generator Builds {0} tests".format(nb_case))
	outfile.write("\n#endif //  {}_INCLUDED\n".format(f_name))
	outfile.close()
	print("Automated Arb_Test Parameter Generator Builds {0} cases".format(nb_case))

	outfile = open(args.arb_decoder_file, 'w')
	outfile.write("//Auto-generated file with arb_src_generator {}\n".format(rev) )
	f_name = os.path.basename(args.arb_decoder_file).upper().replace(".", "_")
	outfile.write("\n#ifndef {}_INCLUDED\n".format(f_name))
	outfile.write("#define {}_INCLUDED\n\n".format(f_name))

	outfile.write("void arb_decoder(const tArbConfig *test)\n")
	outfile.write("{\n\tswitch(test->testid) {\n")
	for f in fct_dict:
		print(f)
		for i in fct_dict[f]['test']:
			outfile.write("\t\tcase {}:\n".format(i))
		outfile.write("\t\t\t {}(".format(f))
		first_param = True
		cnt_int = 0
		cnt_float = 0
		for param in fct_dict[f]['param_type_list']:
			if not first_param:
				outfile.write(" ,")
			if 'int' in param:
				outfile.write("test->param_int[{}]".format(cnt_int))
				cnt_int += 1
			elif param == 'float':
				outfile.write("test->param_float[{}]".format(cnt_float))
				cnt_float += 1
			else:
				raise Exception('ooops')
			first_param = False
		outfile.write(");\n")
		outfile.write("\t\t\t break;\n")
	outfile.write("\t}\n}");
	outfile.write("\n#endif //  {}_INCLUDED\n".format(f_name))
	outfile.close()
