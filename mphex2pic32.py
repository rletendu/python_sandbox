from intelhex import IntelHex
import logging
import argparse
import os
import sys
import json
import configparser

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'
IN="test1.hex"

BFM_START = 0x08000000
BFM_SIZE  = 128*1024
PFM_START = 0x0C000000
PFM_SIZE  = 8*1024*1024
END =0x0C7FFFFF

TEMPLATE_MEMORY = {"BFM":(BFM_START,BFM_START+BFM_SIZE),"PFM":(PFM_START,PFM_START+PFM_SIZE)}
MEMORY_FILE = "memory.ini"


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', action='store_true', help='Activate Debug mode with verbose execution trace information')
	parser.add_argument('--input_file', action='store', help='Input Intel hex file to parse')
	args = parser.parse_args()
	if args.debug:
		logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)
	else:
		logging.basicConfig(level=logging.ERROR, format=LOGGING_FORMAT,)
	log = logging.getLogger(__name__)

	log.debug('Checkinig if memory config fiel exists')
	if not os.path.exists(MEMORY_FILE):
		log.debug("Create default memory config file")
		print("Creating Default {} config memory file ")
		config = configparser.ConfigParser()
		for m in TEMPLATE_MEMORY:
			config.add_section(m)
			config.set(m, 'start', "0x{:08X}".format(TEMPLATE_MEMORY[m][0]))
			config.set(m, 'size', "0x{:08X}".format(TEMPLATE_MEMORY[m][1]-TEMPLATE_MEMORY[m][0]))
		with open(MEMORY_FILE, 'w') as configfile:
			config.write(configfile)

	log.debug("Parse config fie {}".format(MEMORY_FILE))
	config = configparser.ConfigParser()
	cfg = config.read(MEMORY_FILE)
	KNOWN_MEM = {}
	print("Known memory sections from {}:".format(MEMORY_FILE))
	for s in config.sections():
		start = eval(config[s]['start'])
		end = start + eval(config[s]['size'])
		KNOWN_MEM[s] = (start,end)
		print("\t {} -> 0x{:08X}:0x{:08X}".format(s,start,end))

	valid_out_segments = {}
	ih = IntelHex()
	ih.loadhex(args.input_file)
	print("\nParsing input hex file : {}".format(args.input_file))
	print("Range:  0x{:08X}:0x{:08X}".format(ih.minaddr(), ih.maxaddr()))
	for s in ih.segments():
		beg = s[0]
		end = s[1]
		print("#Segment:  0x{:08X}:0x{:08X}".format(beg, end))
		seg_valid = False
		for m in KNOWN_MEM:
			if beg>=KNOWN_MEM[m][0] and beg<=KNOWN_MEM[m][1] and end>=KNOWN_MEM[m][0] and end<=KNOWN_MEM[m][1]:
				seg_valid = True
				log.debug("Found Valid mem seg {}".format(m))
				print("\t -> {} ".format(m),end="")
				segsize = end-beg
				oh= IntelHex()
				log.debug("Loading mem seg {}".format(m))
				for i in range(segsize):
					oh[beg+i] = ih[beg+i]
				valid_out_segments[m] = oh
				print("{} Bytes Valid Memory loaded".format(segsize))
		if not seg_valid:
			print("\t Not supported")

	if not valid_out_segments:
		print("No Valid sections found")
		sys.exit(0)

	print("\nPreparing Output files:")
	out_dir = os.path.abspath(os.path.dirname(args.input_file))
	new_name = os.path.splitext(os.path.basename(args.input_file))[0]
	log.debug("Output dir & filename: {} : {}".format(out_dir,new_name))

	for seg in valid_out_segments:
		f = "{}_{}.hex".format(new_name,seg)
		out_file = os.path.join(out_dir,f)
		print("Generating {} output file {}".format(seg,out_file))
		valid_out_segments[seg].write_hex_file(out_file)

		for s in valid_out_segments[seg].segments():
			beg = s[0]
			end = s[1]
			print("\tSegment:  0x{:08X}:0x{:08X} : {} Bytes".format(beg, end, end-beg))
	

