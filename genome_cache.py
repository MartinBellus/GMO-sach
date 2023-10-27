import requests
from time import sleep
from encryption import encrypt, decrypt
from constants import *
from exceptions import NetworkException
from network import NetworkQuery



genome_cache: dict[str,str] = {}




def fetch_genome(hash: str) -> str:
    if hash in genome_cache:
        return genome_cache[hash]

    # try fetching over network

    encrypted_hash = encrypt(hash)

    query=NetworkQuery("genome", "GET", hash)
    response = query.do_get()
    if not response[0]:
        raise NetworkException
    
    string = response[1]

    string = decrypt(string)

    genome_cache[hash] = string

    return genome_cache[hash]




def upload_genome(hash: str, dna:str) -> None:
    if hash in genome_cache:
        return

    ehash = encrypt(hash)
    edna = encrypt(dna)
    
    query=NetworkQuery("genome", "POST", ehash, edna)
    query.do_query()

    genome_cache[hash] = dna



if __name__ == "__main__":
    print(decrypt(encrypt("HelloWorld1")))
    rook_genome = "AHH HSH HAA CHA CHA CHA HHA SAS AAA AAA AAA".replace(
        " ", "")
    upload_genome(rook_genome)
