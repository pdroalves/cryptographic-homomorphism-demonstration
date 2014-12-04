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
	
def encrypt(pub,m):
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

def decrypt(pub,priv,c,inv=None):
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
