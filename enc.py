import base64
import asn1

encoded = base64.b64encode('data to be encoded'.encode())
print(encoded.decode())
decoded = base64.b64decode(encoded)
print(decoded)


encoder = asn1.Encoder()
encoder.start()
encoder.write('1.2.3', asn1.Numbers.ObjectIdentifier)
encoded_bytes = encoder.output()
print(encoded_bytes)