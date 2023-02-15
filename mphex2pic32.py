from intelhex import IntelHex
import logging
import argparse
import os

LOGGING_FORMAT = '%(asctime)s :: %(levelname)s :: %(name)s :: %(lineno)d :: %(funcName)s :: %(message)s'
IN="C:/Users/M43356/Desktop/certif_riverside/pic32cz_ca80_curiosity_ultra.X.productionMicroB_piononflotant.hex"

BFM_START = 0x08000000
BFM_SIZE  = 128*1024
PFM_START = 0x0C000000
PFM_SIZE  = 8*1024*1024
END =0x0C7FFFFF

#MEMORIES = {"BFM":(BFM_START,BFM_START+BFM_SIZE),"PFM":(PFM_START,PFM_START+PFM_SIZE)}
MEMORIES = {"BFM":(BFM_START,BFM_START+BFM_SIZE)}
#MEMORIES = {"PFM":(PFM_START,PFM_START+PFM_SIZE)}

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--debug', action='store_true', help='Activate Debug mode with verbose execution trace information')
	parser.add_argument('--input_file', action='store', default=IN)
	parser.add_argument('--output_file', action='store', default=None)
	args = parser.parse_args()
	logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT,)	
	log = logging.getLogger(__name__)

	ih = IntelHex()
	oh= IntelHex()

	ih.loadhex(args.input_file)
	print("Input File range:  0x{:08X}:0x{:08X}".format(ih.minaddr(), ih.maxaddr()))

	memsize= 0
	print("Input file content :")
	for s in ih.segments():
		beg = s[0]
		end = s[1]
		print("Segment:  0x{:08X}:0x{:08X}".format(beg, end), end=':')
		valid_memory = False
		for m in MEMORIES:
			if beg>=MEMORIES[m][0] and beg<=MEMORIES[m][1] and end>=MEMORIES[m][0] and end<=MEMORIES[m][1]:
				valid_memory = True
				print(" {} ".format(m),end="")
				break
		if valid_memory:
			segsize = end-beg
			memsize +=segsize
			for i in range(segsize):
				oh[beg+i] = ih[beg+i]
			print(" {} Bytes Valid Memory loaded".format(segsize))
		else:
			print(" Ignored")
		
	if args.output_file is None:
		out_dir = os.path.abspath(os.path.dirname(args.input_file))
		new_name = os.path.splitext(os.path.basename(args.input_file))[0] +"_valid.hex"
		args.output_file = os.path.join(out_dir,new_name)
		print("Output file not spefified, using {}".format(args.output_file))


	print("Generating output file {}".format(args.output_file))
	oh.write_hex_file(args.output_file)
	print("Output file content :")
	for s in oh.segments():
		beg = s[0]
		end = s[1]
		print("Segment:  0x{:08X}:0x{:08X} : {} Bytes".format(beg, end, end-beg))
	

