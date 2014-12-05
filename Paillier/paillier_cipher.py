#!/usr/bin/python
import os
import sys
import getopt
import random
import json
sys.path.append('../') # generate_prime.py is in the parent directory
import generate_prime as Prime

#randrange is mersenne twister and is completely deterministic
#unusable for serious crypto purposes

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

def encrypt(pub,m,n2=None):
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

def decrypt(pub,priv,c):
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