#!/usr/bin/python
import sys
import getopt
import random
import json
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

def squareAndMultiply(base,exponent,modulus):
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

def gerar_chaves(p):
	# Recebe um primo grande p
	alpha = random.randrange(0,p)
	d = random.randrange(2,p-1)
	beta = squareAndMultiply(alpha,d,p)

	# return {
	# 	"public":{
	# 		"p":p,
	# 		"alpha":alpha,
	# 		"beta":beta
	# 	},
	# 	"private":{
	# 		"d":d
	# 	}
	return [alpha,beta,d]
	

def encrypt(p,alpha,beta,m,ke=None,km=None):
	if km is None:
		i = random.randrange(2,p-1)
		ke = squareAndMultiply(alpha,i,p)
		km = squareAndMultiply(beta,i,p)

	ascii = word_to_ascii(m)
	c = []
	for x in ascii:
		c.append( (x*km) % p)

	return c,ke,km

def encrypt_int(p,alpha,beta,m,ke=None,km=None):
	if km is None:
		i = random.randrange(2,p-1)
		ke = squareAndMultiply(alpha,i,p)
		km = squareAndMultiply(beta,i,p)

	c = (m*km) % p

	return c,ke,km

def modinv(x,p):
	return squareAndMultiply(x,p-2,p)

def decrypt(d,p,c,ke,km=None):
	x = []
	if km is None:
		km = squareAndMultiply(ke,d,p)
	inv = modinv(km,p)
	for y in c:
		x.append(y*inv % p)
	return ascii_to_word(x)

def decrypt_int(d,p,c,ke,km=None):
	if km is None:
		km = squareAndMultiply(ke,d,p)
	inv = modinv(km,p)
	m = c*inv % p
	return m

def main(argv):
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hedi:",["encrypt","decrypt","inputfile="])
	except getopt.GetoptError:
		print 'elgamal_cipher.py -m <message>'
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
		print "Gerando primo"
		while p is None:
			try:
				p = Prime.generate_large_prime(1024)
			except Exception,err:
				p = None
				print "Falha ao tentar gerar primo - \%s" % err
		print "Primo gerado!"

		print "Gerando chaves"
		alpha,beta,d = gerar_chaves(p)
		print "Chaves geradas"

		print "Cifrando"
		c,ke = encrypt(p,alpha,beta,m)
		print "Cifra calculada"

		with open("elgamal_public.key","w") as f:
			data = json.dumps({
					"p":p,
					"alpha":alpha,
					"beta":beta
				})
			f.write(data)
		with open("elgamal_private.key","w") as f:
			data = json.dumps({
					"d":d
				})
			f.write(data)
		with open("encrypted_data.dat","w") as f:
			data = json.dumps({
				"message":c,
				"ke":ke
				})
			f.write(data)
	elif mode == "decrypt":

		with open(inputfile,"r") as f:
			data = json.load(f)
			c = data['message']
			ke = data['ke']
		with open("elgamal_public.key","r") as f:
			data = json.load(f)
			p = data['p']
		with open("elgamal_private.key","r") as f:
			data = json.load(f)
			d = data['d']

		print "Mensagem cifrada recuperada: %s" % (decrypt(d,p,c,ke))

if __name__ == "__main__":
	main(sys.argv[1:])