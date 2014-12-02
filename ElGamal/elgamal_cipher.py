#!/usr/bin/python
import sys
import getopt
import random
import json
import os
sys.path.append('../') # generate_prime.py is in the parent directory
import generate_prime as Prime

def is_int(x):
	try:
		int(x)
		return True
	except:
		return False

def word_to_ascii(w):
	if is_int(w):
		return [int(w)]
	else:
		return [ord(x) for x in w]

def ascii_to_word(a):
	try:
		return ''.join(chr(x) for x in a)
	except:
		return a

def square_and_multiply(base,exponent,modulus):
	#Converting the exponent to its binary form
	binaryExponent = []
	while exponent != 0:
		binaryExponent.append(exponent%2)
		exponent = exponent/2
	#Appllication of the square and multiply algorithm
	result = 1
	binaryExponent.reverse()
	for i in binaryExponent:
		if i == 0:
			result = (result*result) % modulus
		else:
			result = (result*result*base) % modulus
	return result

def generate_keys(p):
	#
	# Receives a big prime p
	#
	# Public key: (p,alpha,beta)
	# Private key: (d) 

	alpha = random.randrange(0,p)
	d = random.randrange(2,p-1)
	beta = square_and_multiply(alpha,d,p)

	return {"pub":{
				"p":p,
				"alpha":alpha,
				"beta":beta},
			"priv":{
			 "d":d
			 }
		   }

def modinv(x,p):
	#
	# Computes the moduler inversion of x ** p-2 mod p
	#
	return square_and_multiply(x,p-2,p)
	
def encrypt_string(pub,m):
	#
	# 	Converts all characters from a string m
	#  to an array of integers, encrypts all elements and
	#  add ke and km to public key
	#

	assert pub.has_key('p')
	assert pub.has_key('alpha')
	assert pub.has_key('beta')
	p = pub['p']
	alpha = pub['alpha']
	beta = pub['beta']

	if not pub.has_key('ke') or not pub.has_key('km'): 
		i = random.randrange(2,p-1)
		ke = square_and_multiply(alpha,i,p)
		km = square_and_multiply(beta,i,p)
		pub['ke'] = ke
		pub['km'] = km
	else:
		ke = pub['ke']
		km = pub['km']

	ascii = word_to_ascii(m)
	c = []
	for x in ascii:
		c.append(encrypt_int(pub,x))

	return c


def decrypt_string(pub,priv,c):
	#
	#  Receives an array of encrypted integers,
	# decrypts each integer, convert it to an ascii character and 
	# append it in a string
	#

	assert pub.has_key('p')
	assert pub.has_key('ke')
	assert priv.has_key('d')
	p = pub['p']
	ke = pub['ke']
	d = priv['d']

	x = []
	if not pub.has_key('km'):
		km = square_and_multiply(ke,d,p)
	else:
		km = pub['km']

	inv = modinv(km,p)
	for y in c:
		x.append(decrypt_int(pub,priv,y,inv=inv))
	return ascii_to_word(x)

def encrypt_int(pub,m):
	#
	# Encrypts a single integer
	#

	assert is_int(m)
	assert pub.has_key('p')
	assert pub.has_key('alpha')
	assert pub.has_key('beta')
	p = pub['p']
	alpha = pub['alpha']
	beta = pub['beta']

	if not pub.has_key('ke') or not pub.has_key('km'): 
		i = random.randrange(2,p-1)
		ke = square_and_multiply(alpha,i,p)
		km = square_and_multiply(beta,i,p)
		pub['ke'] = ke
		pub['km'] = km
	else:
		ke = pub['ke']
		km = pub['km']

	c = (m*km) % p

	return c

def decrypt_int(pub,priv,c,inv):
	#
	# Decrypts a single integer
	#
	assert is_int(c)
	assert pub.has_key('p')
	assert pub.has_key('ke')
	assert priv.has_key('d')
	p = pub['p']
	ke = pub['ke']
	km = pub['km']
	d = priv['d']

	if not pub.has_key('km'):
		km = square_and_multiply(ke,d,p)
	else:
		km = pub['km']
	if not inv:
		inv = modinv(km,p)
	return c*inv % p

def main(argv):
	pub_file_name = None
	priv_file_name = None
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hedi:",["encrypt","decrypt","inputfile="])
	except getopt.GetoptError:
		print 'elgamal_cipher.py -i <inputfile> [-e <encrypt_mode> |-d <decrypt_mode>] '
		sys.exit(2)
	# process options
	for opt, arg in opts: 
		if opt == '-h':
			print 'elgamal_cipher.py -i <inputfile> [-e <encrypt_mode> |-d <decrypt_mode>] '
			sys.exit()
		elif opt in ("-e", "--encrypt"):
			mode = "encrypt"
		elif opt in ("-d","--decrypt"):
			mode = "decrypt"
		elif opt in ("-i","--inputfile"):
			inputfile = arg
		elif opt in ("--pub"):
			pub_file_name = "elgamal_public.key"
		elif opt in ("--priv"):
			priv_file_name = "elgamal_private.key"

	if mode == "encrypt":

		with open(inputfile,"r") as f:
			m = f.read()

		p = None
		print "Generating a prime..."
		while p is None:
			try:
				p = Prime.generate_large_prime(1024)
			except Exception,err:
				p = None
				print "Failure on prime generation - \%s" % err
		print "Prime found!"

		print "Generating keys..."
		keys = generate_keys(p)
		print "The keys were generated."

		print "Encrypting..."
		c = encrypt_string(keys['pub'],m)
		print "Encryption done."

		# Saving data
		if not pub_file_name:
			pub_file_name = "elgamal_public.key"
		if not priv_file_name:
			priv_file_name = "elgamal_private.key"
		encrypted_data_file_name = os.path.splitext(inputfile)[0]+"_encrypted.txt"
		with open(pub_file_name,"w") as f:
			data = json.dumps(keys['pub'])
			f.write(data)
			print "Public key stored in %s"%pub_file_name
		with open(priv_file_name,"w") as f:
			data = json.dumps(keys['priv'])
			f.write(data)
			print "Private key stored in %s"%priv_file_name
		with open(encrypted_data_file_name,"w") as f:
			data = json.dumps({
				"message":c
				})
			f.write(data)
			print "Encrypted message stored in %s"%encrypted_data_file_name

	elif mode == "decrypt":

		if not pub_file_name:
			pub_file_name = "elgamal_public.key"
		if not priv_file_name:
			priv_file_name = "elgamal_private.key"
		decrypted_data_file_name = inputfile.replace("_encrypted.","_decrypted.")

		with open(inputfile,"r") as f:
			data = json.load(f)
			c = data['message']
		with open(pub_file_name,"r") as f:
			pub = json.load(f)
		with open(priv_file_name,"r") as f:
			priv = json.load(f)
			
		print "Data loaded. Decrypting..."

		with open(decrypted_data_file_name,"w") as f:
			f.write(decrypt_string(pub,priv,c))

		print "Encrypted message recovered and stored in %s." %decrypted_data_file_name 

if __name__ == "__main__":
	main(sys.argv[1:])