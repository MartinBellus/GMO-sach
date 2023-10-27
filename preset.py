from constants import *
import requests
from encryption import encrypt, decrypt
from exceptions import NetworkException
from time import sleep
from network import NetworkQuery
from genome import Genome
import hashlib

class Preset:
    def __init__(self, genomes:list[Genome]):
        self.genomes=genomes
        assert len(genomes) <= BOARD_X, "There must be at most {BOARD_X} genomes in a preset"

        self.hashes=[]
        for i in self.genomes:
            self.hashes.append(i.hash())
        self.string = "-".join(self.hashes)
        
    
    def hash(self):
        return hashlib.sha256(self.string.encode()).hexdigest()[:6]
        

    @classmethod
    def fetch_preset(cls, hash: str):

        # try fetching over network

        encrypted_hash = encrypt(hash)

        query = NetworkQuery("preset", "GET", encrypted_hash)

        response = query.do_query()
        
        if not response[0]:
            raise NetworkException

        string = response[1]
        string = decrypt(string)

        hashes = string.split("-")

        return cls([Genome.from_hash(i) for i in hashes])
    
    def save(self):
        encrypted_string = encrypt(self.string)
        encrypted_hash =encrypt(self.hash())
        
        query=NetworkQuery("preset", "POST", encrypted_hash, encrypted_string)
        
        response = query.do_query()
        if not response[0]:
            raise NetworkException
        
        
    
