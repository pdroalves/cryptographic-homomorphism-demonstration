#!/usr/bin/python
import sys
import getopt
import random
import json
import os
sys.path.append('../') # generate_prime.py is in the parent directory
import generate_prime as Prime
import auxiliar as Aux

#randrange is mersenne twister and is completely deterministic
#unusable for serious crypto purposes

def generate_keys(p):
	#
	# Receives a big prime p
	#
	# Public key: (p,alpha,beta)
	# Private key: (d) 

	alpha = random.randrange(1,p) # if |G| is prime, then all elements a not 1 \in G are primitives
	d = random.randrange(2,p-1)# from 2 to p-2
	beta = Aux.square_and_multiply(alpha,d,p)

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
	# Computes the moduler inversion of x ** p-2 mod p,
	# for p prime
	#
	return Aux.square_and_multiply(x,p-2,p)
	
def encrypt(pub,m,km=None):
	#
	# Encrypts a single integer
	#

	assert Aux.is_int(m)
	assert pub.has_key('p')
	assert pub.has_key('alpha')
	assert pub.has_key('beta')
	p = pub['p']
	alpha = pub['alpha']
	beta = pub['beta']

	if not km:
		i = random.randrange(2,p-1)
		ke = Aux.square_and_multiply(alpha,i,p)
		km = Aux.square_and_multiply(beta,i,p)

		c = (m*km) % p
		return c,ke
	else:

		c = (m*km) % p
		return c,None

def decrypt(pub,priv,x,inv=None):
	#
	# Decrypts a single integer
	#
	assert pub.has_key('p')
	assert priv.has_key('d')
	assert x.has_key('c')
	assert x.has_key('ke')
	p = pub['p']
	d = priv['d']

	c = x['c']
	ke = x['ke']

	km = Aux.square_and_multiply(ke,d,p)

	if not inv:
		inv = modinv(km,p)
	return c*inv % p

def generate_lookup_table(g,p,a=0,b=10**3):
	#
	# Receives an base g, prime p, a public key pub and a interval [a,b],
	# computes and encrypts all values g**i mod p for a <= i <= b and 
	# returns a lookup table
	#
	table = {}
	for i in xrange(a,b):
		c = Aux.square_and_multiply(g,i,p)
		table[c] = i
	return table