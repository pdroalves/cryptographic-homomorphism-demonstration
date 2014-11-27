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

def gerar_chaves(p,q):
	n = p*q
	g = n+1
	l = (p-1)*(q-1)# == phi(n)
	mi = squareAndMultiply(l,l-1,n)
	return n,g,l,mi

def encrypt(n,g,m):
	ascii = word_to_ascii(m)
	c = []
	n2 = n*n
	for x in ascii:
		assert x < n
		r = random.randrange(1,n)
		c.append(squareAndMultiply(g,x,n2)*squareAndMultiply(r,n,n2))

	return c

def decrypt(c,n,l,mi):
	x = []
	charmical_function = lambda u,n: (u-1)/n
	n2 = n*n
	for y in c:
		x.append(charmical_function(squareAndMultiply(y,l,n2),n)*mi % n)
	return ascii_to_word(x)

def encrypt_int(n,g,m):
	assert m < n
	n2 = n*n
	r = random.randrange(1,n)
	c = squareAndMultiply(g,m,n2)*squareAndMultiply(r,n,n2)
	return c

def decrypt_int(c,n,l,mi):
	charmical_function = lambda u,n: (u-1)/n
	n2 = n*n
	m = charmical_function(squareAndMultiply(c,l,n2),n)*mi % n
	return m

def main(argv):
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
		print "Gerando primos"
		while p is None or q is None:
			try:
				p = Prime.generate_large_prime(512)
				q = Prime.generate_large_prime(512)

				assert p != q

			except Exception,err:
				p = None
				q = None
				print "Falha ao tentar gerar primo - \%s" % err
		print "Primos gerados!"

		print "Gerando chaves"
		n,g,l,mi = gerar_chaves(p,q)
		print "Chaves geradas"

		print "Cifrando"
		c = encrypt(n,g,m)
		print "Cifra calculada"

		with open("paillier_public.key","w") as f:
			data = json.dumps({
					"n":n,
					"g":g
				})
			f.write(data)
		with open("paillier_private.key","w") as f:
			data = json.dumps({
					"lambda":l,
					"mi":mi
				})
			f.write(data)
		with open("encrypted_data.dat","w") as f:
			data = json.dumps({
				"message":c
				})
			f.write(data)
	elif mode == "decrypt":

		with open(inputfile,"r") as f:
			data = json.load(f)
			c = data['message']
		with open("paillier_public.key","r") as f:
			data = json.load(f)
			n = data['n']
			g = data['g']
		with open("paillier_private.key","r") as f:
			data = json.load(f)
			l = data['lambda']
			mi = data['mi']

		print "Mensagem cifrada recuperada: %s" % (decrypt(c,n,l,mi))
if __name__ == "__main__":
	main(sys.argv[1:])