from constants import *
import requests
from encryption import encrypt, decrypt
from exceptions import NetworkException
from time import sleep
from network import NetworkQuery
from genome import Genome
import hashlib

class Preset:
    def __init__(self, hashes:list[str]):
        self.hashes=hashes
        assert len(hashes) <= BOARD_X, "There must be at most {BOARD_X} genomes in a preset"

        self.genomes=[]
        for i in self.hashes:
            self.genomes.append(Genome.from_hash(i))
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

        return cls(hashes)
    
    def save(self):
        encrypted_string = encrypt(self.string)
        encrypted_hash =encrypt(self.hash())
        
        query=NetworkQuery("preset", "POST", encrypted_hash, encrypted_string)
        
        response = query.do_query()
        if not response[0]:
            raise NetworkException
        
        
    
