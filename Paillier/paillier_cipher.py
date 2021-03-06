#!/usr/bin/python
import os
import sys
import getopt
import random
import json
sys.path.append('../') # generate_prime.py is in the parent directory
import generate_prime as Prime
import auxiliar as Aux

#randrange is mersenne twister and is completely deterministic
#unusable for serious crypto purposes

def generate_keys(p,q):
	n = p*q
	g = n+1
	l = (p-1)*(q-1)# == phi(n)
	
	return {"pub":{
				"n":n,
				"g":g},
			"priv":{
			 "lambda":l
			 }
		   }

def encrypt(pub,m,n2=None):
	assert Aux.is_int(m)
	assert pub.has_key('n')
	assert pub.has_key('g')
	n = pub['n']
	g = pub['g']

	assert m < n
	if not n2:
		n2 = n*n
	r = random.randrange(1,n)
	c = Aux.square_and_multiply(g,m,n2)*Aux.square_and_multiply(r,n,n2)
	return c

def decrypt(pub,priv,c):
	assert Aux.is_int(c)	
	assert pub.has_key('n')
	assert pub.has_key('g')
	assert priv.has_key('lambda')
	n = pub['n']
	g = pub['g']
	l = priv['lambda']
	
	mi = Aux.square_and_multiply(l,l-1,n)

	charmical_function = lambda u,n: (u-1)/n
	n2 = n*n
	m = charmical_function(Aux.square_and_multiply(c,l,n2),n)*mi % n
	return m