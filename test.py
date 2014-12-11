#!/usr/bin/python
import random
import unittest
import generate_prime as Prime
from ElGamal import elgamal_cipher as ElGamal
from Paillier import paillier_cipher as Paillier

class TestSequenceFunctions(unittest.TestCase):

    def test_miller_rabin(self):
        # Miller-Rabin test gives no guarantee that a number is a truly prime.
        # However, it should give guarantee that a number isn't prime.
        #

        print "Test: Miller-Rabin"

        # Load the first 10.000 primes from http://primes.utm.edu/lists/small/10000.txt
        with open("10000primes.dat") as f:
            data = f.readlines()
            known_primes = [int(x) for x in data]

        higher = 104729 # higher known prime
        for n in xrange(10,higher):
            if not Prime.miller_rabin(n):
                # If our test says a number n isn't prime, we check if it really isn't in our known prime list
                self.assertFalse(n in known_primes)

    def test_elgamal(self):
        #
        # Tests if this cipher can encrypt and decrypt all values up to 10**3
        #

        print "Test: ElGamal cipher"

        key_size = 1024
        p = None
        while p is None:
            try:
                p = Prime.generate_large_prime(key_size)
            except Exception,err:
                p = None
                print "Failure on prime generation - \%s" % err
        
        keys = ElGamal.generate_keys(p)
        for n in xrange(1,10**3):
            c,ke = ElGamal.encrypt(keys['pub'],n)
            self.assertNotEqual(c,n)
            self.assertEqual(ElGamal.decrypt(keys['pub'],keys['priv'],{'c':c,'ke':ke}),n)

    def test_paillier(self):
        #
        # Tests if this cipher can encrypt and decrypt all values up to 10**3
        #

        print "Test: Paillier cipher"

        key_size = 512 # We use a smaller key than elgamal to be able to complete this test in less than 1 minute

        p = None
        q = None
        while p is None:
            try:
                p = Prime.generate_large_prime(key_size)
            except Exception,err:
                p = None
                print "Failure on prime generation - \%s" % err
        while q is None:
            try:
                q = Prime.generate_large_prime(key_size)
            except Exception,err:
                q = None
                print "Failure on prime generation - \%s" % err
        
        keys = Paillier.generate_keys(p,q)
        for n in xrange(10**3):
            c = Paillier.encrypt(keys['pub'],n)
            self.assertNotEqual(c,n)
            self.assertEqual(Paillier.decrypt(keys['pub'],keys['priv'],c),n)
if __name__ == '__main__':
    unittest.main()