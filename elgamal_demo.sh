#!/bin/bash
./generate_candidate_list.py -c elgamal 
./add_votes.py -c elgamal --vote="1 3 2 1 7 8" 
./decrypt_votes.py -c elgamal
