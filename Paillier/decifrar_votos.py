#!/usr/bin/python
import json
import paillier_cipher as Paillier
import generate_prime as Prime

with open("votos_cifrados.dat","r") as f:
	votos_cifrados = json.load(f)
with open("paillier_public.key","r") as f:
	data = json.load(f)
	n = data['n']
	g = data['g']
with open("paillier_private.key","r") as f:
	data = json.load(f)
	l = data['lambda']
	mi = data['mi']
votos = {}

for candidato in votos_cifrados.keys():
	m = Paillier.decrypt_int(
							c=votos_cifrados[candidato],
							n=n,
							l=l,
							mi=mi
						)
	votos[candidato] = m

with open("votos.dat","w") as f:
	f.write(json.dumps(votos,indent=4))