#!/usr/bin/python
import json
import sys
import getopt
import generate_prime as Prime

def main(argv):
	inputfile = "encrypted_votes.dat"
	pub_file_name = "public.key"
	data = None
	votes = None
	# parse command line options
	try:
		opts, args = getopt.getopt(argv, "hc:i:v:a:",["cipher=","inputfile=","vote=","pub=","priv="])
	except getopt.GetoptError:
		print 'add_votes.py -c <cipher> -i <inputfile> -v <vote> -a <pub>'
		sys.exit(2)
	# process options
	cipher_loaded = False
	for opt, arg in opts: 
		if opt == '-h':
			print 'add_votes.py -c <cipher> -i <inputfile> -v <vote> -a <pub>'
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
		elif opt in ("-v","--vote"):
			votes = [int(x) for x in arg.split(" ")]
		elif opt in ("-a","--pub"):
			pub_file_name = arg

	if not cipher_loaded:
		raise Exception("Unknown cipher.")
	if not votes:
		raise Exception("Invalid vote.")

	with open(inputfile,"r") as f:
		data = json.load(f)
	with open(pub_file_name,"r") as f:
		pub = json.load(f)

	assert data
	assert data.has_key('candidates')
	assert data.has_key('voting_table')

	candidates = data['candidates']
	early_voting_table = data['voting_table']

	for index,vote in enumerate(votes):
		encrypted_vote = Cipher.encrypt_int(pub,vote)
		if cipher_loaded == "elgamal":
			early_voting_table[index] = early_voting_table[index] + encrypted_vote
		elif cipher_loaded == "paillier":
			early_voting_table[index] = early_voting_table[index] * encrypted_vote

	with open(inputfile,"w") as f:
		data = json.dumps({'candidates':candidates,'voting_table':early_voting_table})
		f.write(data)
		print "Encrypted votes stored in %s"%inputfile



if __name__ == "__main__":
	main(sys.argv[1:])