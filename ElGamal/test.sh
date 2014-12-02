#!/bin/bash

echo -e "Encrypting...\n"
./elgamal_cipher.py -e -i lorem_ipsum.txt
echo -e "\nDescrypting...\n"
./elgamal_cipher.py -d -i lorem_ipsum_encrypted.txt
echo -e "\nTesting...\n"
if cmp lorem_ipsum.txt lorem_ipsum_decrypted.txt &> /dev/null;then
   echo "Correct!"
else
   echo "Failure!"
fi 
