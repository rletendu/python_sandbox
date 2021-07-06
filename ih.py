from intelhex import IntelHex

ih = IntelHex()
data = []
for i in range(10):
	data.append(i)

for i in range(len(data)):
	ih[i+0x20000000]=data[i]

ih.write_hex_file('toto.hex')
ih.tobinfile('toto.bin')
print(ih)

