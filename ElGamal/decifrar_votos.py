#!/usr/bin/python
import json
import elgamal_cipher as ElGamal
import generate_prime as Prime

with open("votos_cifrados.dat","r") as f:
	votos_cifrados = json.load(f)
with open("elgamal_public.key","r") as f:
	data = json.load(f)
	p = data['p']
	alpha = data['alpha']
	beta = data['beta']
	ke = data['ke']
with open("elgamal_private.key","r") as f:
	data = json.load(f)
	d = data['d']
	km = data['km']
votos = {}

for candidato in votos_cifrados.keys():
	m = ElGamal.decrypt_int(
						d=d,
						p=p,
						c=votos_cifrados[candidato],
						ke=ke,
						km=km)
	votos[candidato] = m

with open("votos.dat","w") as f:
	f.write(json.dumps(votos,indent=4))