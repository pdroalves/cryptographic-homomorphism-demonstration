#!/usr/bin/python
import json
import sys
import getopt
import random
import generate_prime as Prime

def main(argv):
	pub_file_name = "public.key"
	priv_file_name = "private.key"
	encrypted_data_file_name = "encrypted_votes.json"

	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hc:",["cipher="])
	except getopt.GetoptError:
		print 'generate_candidate_list.py -c <cipher>'
		sys.exit(2)
	# process options
	cipher_loaded = False
	for opt, arg in opts: 
		if opt == '-h':
			print 'generate_candidate_list.py -c <cipher>'
			sys.exit()
		elif opt in ("-c", "--cipher"):
			if arg == "elgamal":
				import ElGamal.elgamal_cipher as Cipher
				cipher_loaded = "elgamal"
			elif arg == "paillier":
				import Paillier.paillier_cipher as Cipher
				cipher_loaded = "paillier"

	if not cipher_loaded:
		raise Exception("Unknown cipher")

	print "Using %s encryption scheme" % cipher_loaded

	candidates = [
		"Bruce Wayne", 
		"Peter Parker",
		"Clark Kent",
		"Hal Jordan",
		"Tony Stark",
		"Steve Rogers",]
	candidate_list = {}

	key_size = 1024

	p = None
	print "Generating a prime..."
	while p is None:
		try:
			p = Prime.generate_large_prime(key_size)
		except Exception,err:
			p = None
			print "Failure on prime generation - \%s" % err
	if cipher_loaded == "paillier":
		q = None
		while q is None:
			try:
				q = Prime.generate_large_prime(key_size)
			except Exception,err:
				q = None
				print "Failure on prime generation - \%s" % err

	print "Prime found!"

	print "Generating keys..."
	if cipher_loaded == "elgamal":
		keys = Cipher.generate_keys(p)

	elif cipher_loaded == "paillier":
		keys = Cipher.generate_keys(p,q)
	print "The keys were generated."

	# Initialize all candidates with zero votes
	print ""
	for index,candidate in enumerate(candidates):
		candidate_list[candidate] = index
		print "Candidate: %s - %d" % (candidate,index)
	print ""
	print "Encrypting..."
	# Encrypts the voting table
	voting_table = []
	for index in range(len(candidates)):
		if cipher_loaded == "elgamal":
			c,ke = Cipher.encrypt(keys['pub'],int(1))#This is equal to encrypts g**0 mod p
			voting_table.append({'c':c,'ke':ke}) 
		else:
			voting_table.append(Cipher.encrypt(keys['pub'],int(0)))
	print "Encryption done."

	# Saving data
	with open(pub_file_name,"w") as f:
		json.dump(keys['pub'],f)
		print "Public key stored in %s"%pub_file_name
	with open(priv_file_name,"w") as f:
		json.dump(keys['priv'],f)
		print "Private key stored in %s"%priv_file_name
	with open(encrypted_data_file_name,"w") as f:
		json.dump({'candidates':candidate_list,'voting_table':voting_table},f)
		print "Encrypted votes stored in %s"%encrypted_data_file_name

if __name__ == "__main__":
	main(sys.argv[1:])