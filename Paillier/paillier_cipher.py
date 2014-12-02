#!/usr/bin/python
import os
import sys
import getopt
import random
import json
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

def generate_keys(p,q):
	n = p*q
	g = n+1
	l = (p-1)*(q-1)# == phi(n)
	mi = square_and_multiply(l,l-1,n)
	return {"pub":{
				"n":n,
				"g":g},
			"priv":{
			 "lambda":l,
			 "mi":mi
			 }
		   }

def encrypt_string(pub,m):
	#
	# 	Converts all characters from a string m
	#  to an array of integers, encrypts all elements
	#

	assert pub.has_key('n')
	assert pub.has_key('g')
	n = pub['n']
	g = pub['g']

	ascii = word_to_ascii(m)
	c = []
	n2 = n*n
	for x in ascii:
		assert x < n
		c.append(encrypt_int(pub,x,n2=n2))

	return c

def decrypt_string(pub,priv,c):	
	assert pub.has_key('n')
	assert pub.has_key('g')
	assert priv.has_key('lambda')
	assert priv.has_key('mi')
	n = pub['n']
	g = pub['g']
	l = priv['lambda']
	mi = priv['mi']

	x = []
	charmical_function = lambda u,n: (u-1)/n
	n2 = n*n
	for y in c:
		x.append(decrypt_int(pub,priv,y))
	return ascii_to_word(x)

def encrypt_int(pub,m,n2=None):
	assert is_int(m)
	assert pub.has_key('n')
	assert pub.has_key('g')
	n = pub['n']
	g = pub['g']

	assert m < n
	if not n2:
		n2 = n*n
	r = random.randrange(1,n)
	c = square_and_multiply(g,m,n2)*square_and_multiply(r,n,n2)
	return c

def decrypt_int(pub,priv,c):
	assert is_int(c)	
	assert pub.has_key('n')
	assert pub.has_key('g')
	assert priv.has_key('lambda')
	assert priv.has_key('mi')
	n = pub['n']
	g = pub['g']
	l = priv['lambda']
	mi = priv['mi']

	charmical_function = lambda u,n: (u-1)/n
	n2 = n*n
	m = charmical_function(square_and_multiply(c,l,n2),n)*mi % n
	return m

def main(argv):
	pub_file_name = None
	priv_file_name = None
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hedi:",["encrypt","decrypt","inputfile="])
	except getopt.GetoptError:
		print 'paillier_cipher.py -m <message>'
		sys.exit(2)
	# process options
	for opt, arg in opts: 
		if opt == '-h':
			print 'test.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-e", "--encrypt"):
			mode = "encrypt"
		elif opt in ("-d","--decrypt"):
			mode = "decrypt"
		elif opt in ("-i","--inputfile"):
			inputfile = arg

	if mode == "encrypt":

		with open(inputfile,"r") as f:
			m = f.read()

		p = None
		q = None
		print "Generating primes..."
		while p is None or q is None:
			try:
				p = Prime.generate_large_prime(256)
				q = Prime.generate_large_prime(256)

				assert p != q

			except Exception,err:
				p = None
				q = None
				print "Failure on prime generation - \%s" % err
		print "Prime found!"

		print "Generating keys..."
		keys = generate_keys(p,q)
		print "The keys were generated."

		print "Encrypting..."
		c = encrypt_string(keys['pub'],m)
		print "Encryption done."

		if not pub_file_name:
			pub_file_name = "paillier_public.key"
		if not priv_file_name:
			priv_file_name = "paillier_private.key"
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
			pub_file_name = "paillier_public.key"
		if not priv_file_name:
			priv_file_name = "paillier_private.key"
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