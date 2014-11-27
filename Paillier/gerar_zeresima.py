#!/usr/bin/python
import json
import paillier_cipher as Paillier
import generate_prime as Prime

candidatos = [
	"Bruce Wayne", 
	"Peter Parker",
	"Clark Kent",
	"Hal Jordan",
	"Tony Stark",
	"Steve Rogers"]

p = None
q = None
print "Gerando primos"
while p is None or q is None:
	try:
		p = Prime.generate_large_prime(512)
		q = Prime.generate_large_prime(512)

		assert p != q

	except Exception,err:
		p = None
		q = None
		print "Falha ao tentar gerar primo - \%s" % err
print "Primos gerados!"

print "Gerando chaves"
n,g,l,mi = Paillier.gerar_chaves(p,q)
print "Chaves geradas"

zeresima = {}
print "Cifrando"
for candidato in candidatos:
	c = Paillier.encrypt_int(n,g,0)
	zeresima[candidato] = c
print "Cifra calculada"

with open("votos_cifrados.dat","w") as f:
	f.write(json.dumps(zeresima,indent=4))
with open("paillier_public.key","w") as f:
	data = json.dumps({
			"n":n,
			"g":g
		})
	f.write(data)
with open("paillier_private.key","w") as f:
	data = json.dumps({
			"lambda":l,
			"mi":mi
		})
	f.write(data)