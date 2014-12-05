#!/usr/bin/python
import json
import sys
import getopt
import generate_prime as Prime

def main(argv):
	inputfile = "encrypted_votes.json"
	output = "decrypted_votes.json"
	pub_file_name = "public.key"
	priv_file_name = "private.key"
	data = None
	votes = None
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hc:i:o:v:a:",["cipher=","inputfile=","output","pub=","priv="])
	except getopt.GetoptError:
		print 'decrypt_votes.py -c <cipher> -i <inputfile> -o <output> -a <pub> -b <priv>'
		sys.exit(2)
	# process options
	cipher_loaded = False
	for opt, arg in opts: 
		if opt == '-h':
			print 'decrypt_votes.py -c <cipher> -i <inputfile> -o <output> -a <pub> -b <priv>'
			sys.exit()
		elif opt in ("-c", "--cipher"):
			if arg == "elgamal":
				import ElGamal.elgamal_cipher as Cipher
				cipher_loaded = "elgamal"
			elif arg == "paillier":
				import Paillier.paillier_cipher as Cipher
				cipher_loaded = "paillier"
		elif opt in ("-i","--inputfile"):
			inputfile = arg
		elif opt in ("-o","--output"):
			output = arg
		elif opt in ("-a","--pub"):
			pub_file_name = arg
		elif opt in ("-b","--priv"):
			priv_file_name = arg

	if not cipher_loaded:
		raise Exception("Unknown cipher.")
	
	with open(inputfile,"r") as f:
		data = json.load(f)
	with open(pub_file_name,"r") as f:
		pub = json.load(f)
	with open(priv_file_name,"r") as f:
		priv = json.load(f)
	
	# Generates a lookup table to help decryption 

	assert data
	assert data.has_key('candidates')
	assert data.has_key('voting_table')

	candidates = data['candidates']
	ciphertext_voting_table = data['voting_table']

	if cipher_loaded == "elgamal":
		print "Generating lookup table"
		lookup_table = Cipher.generate_lookup_table(pub['alpha'],pub['p'],a=0,b=10**3)
		plaintext_voting_table = [lookup_table[Cipher.decrypt(pub,priv,x)] for x in ciphertext_voting_table]
	else:
		plaintext_voting_table = [Cipher.decrypt(pub,priv,x) for x in ciphertext_voting_table]

	candidates_sorted = sorted(candidates,key=lambda x:plaintext_voting_table[candidates[x]],reverse=True)

	for candidate in candidates_sorted:
		print "%s - %d votes" % (candidate,plaintext_voting_table[candidates[candidate]])

	with open(output,"w") as f:
		data = json.dumps({'candidates':candidates,'voting_table':plaintext_voting_table})
		f.write(data)
		print "Decrypted votes stored in %s"%output



if __name__ == "__main__":
	main(sys.argv[1:])