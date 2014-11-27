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
	mc = votos_cifrados[candidato]

	vc = Paillier.encrypt_int(	n,
								g,
								100
							)

	votos[candidato] = mc*vc

with open("votos_cifrados.dat","w") as f:
	f.write(json.dumps(votos,indent=4))