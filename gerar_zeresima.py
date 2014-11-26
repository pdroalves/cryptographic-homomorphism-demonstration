#!/usr/bin/python
import json
import elgamal_cipher as ElGamal
import generate_prime as Prime

candidatos = [
	"Bruce Wayne", 
	"Peter Parker",
	"Clark Kent",
	"Hal Jordan",
	"Tony Stark",
	"Steve Rogers"]
zeresima = {}

for candidato in candidatos:
	zeresima[candidato] = 0

p = None
print "Gerando primo"
while p is None:
	try:
		p = Prime.generate_large_prime(1024)
	except Exception,err:
		p = None
		print "Falha ao tentar gerar primo - \%s" % err
print "Primo gerado!"

print "Gerando chaves"
alpha,beta,d = ElGamal.gerar_chaves(p)
print "Chaves geradas"

print "Cifrando"
c,ke,km = ElGamal.encrypt_int(p,alpha,beta,0)
print "Cifra calculada"

with open("votos_cifrados.dat","w") as f:
	f.write(json.dumps(zeresima,indent=4))
with open("elgamal_public.key","w") as f:
	data = json.dumps({
			"p":p,
			"alpha":alpha,
			"beta":beta,
			"ke":ke
		})
	f.write(data)
with open("elgamal_private.key","w") as f:
	data = json.dumps({
			"d":d,
			"km":km
		})
	f.write(data)