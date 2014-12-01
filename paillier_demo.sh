#!/bin/bash
./generate_candidate_list.py -c paillier 
./add_votes.py -c paillier --vote="1 3 2 1 7 8" 
./decrypt_votes.py -c paillier
