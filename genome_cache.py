from genome import *
import requests
from time import sleep


class NetworkException(Exception):
    pass


class GenomeNotFound(Exception):
    pass


genome_cache = {}

HTTP_URL = "http://localhost:5000/"

ENCRYPTION_KEY = "1gSD89IsdfjIie4gs454G2werg3W23gw3GW8WGwg5wG8sU4Euer3434urt6u4s64g8KHGWERg64sfg"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
LETTER_TO_INDEX = {letter: index for index, letter in enumerate(ALPHABET)}
ALPHABET_LENGTH = len(ALPHABET)


def encrypt(string: str) -> str:
    assert all(
        i in LETTER_TO_INDEX for i in string), f"Only can encrypt characters {ALPHABET}"

    # prefix sum and then shift by key_id
    l = [LETTER_TO_INDEX[c] for c in string]
    for i in range(1, len(l)):
        l[i] += l[i-1]
        l[i] %= ALPHABET_LENGTH

    keyind = 0
    for i in range(len(l)):
        l[i] = (l[i]+LETTER_TO_INDEX[ENCRYPTION_KEY[keyind]]) % ALPHABET_LENGTH
        keyind = (keyind+1) % len(ENCRYPTION_KEY)

    return "".join(ALPHABET[i] for i in l)


def decrypt(string: str):
    assert all(
        i in LETTER_TO_INDEX for i in string), f"Only can encrypt characters {ALPHABET}"

    l = [LETTER_TO_INDEX[i] for i in string]

    keyind = 0
    for i in range(len(l)):
        l[i] = (l[i]-LETTER_TO_INDEX[ENCRYPTION_KEY[keyind]]) % ALPHABET_LENGTH
        keyind = (keyind+1) % len(ENCRYPTION_KEY)

    nl = [l[0]]
    for i in range(1, len(l)):
        nl.append(l[i]-l[i-1])

    return "".join(ALPHABET[i] for i in nl)


QUERY_ATTEMPTS = 5

TIMEOUT = 1


def fetch_genome(hash: str) -> Genome:
    if hash in genome_cache:
        return genome_cache[hash]

    # try fetching over network

    encrypted_hash = encrypt(hash)

    string = None
    for i in range(QUERY_ATTEMPTS):
        try:
            response = requests.get(HTTP_URL+encrypted_hash, timeout=TIMEOUT)
            if response:
                string = response.text
                break
        except requests.exceptions.Timeout:
            pass
        except:
            raise NetworkException
        sleep(0.1 * 2**i)

    if string is None:
        raise NetworkException

    if string.count("!"):
        raise GenomeNotFound

    string = decrypt(string)

    genome_cache[hash] = Genome(string)

    return genome_cache[hash]


POST_ATTEMPTS = 5

upload_queue = []


def empty_queue():
    while len(upload_queue):
        done = False
        current = upload_queue[0]

        for i in range(POST_ATTEMPTS):
            try:
                response = requests.post(
                    HTTP_URL+current["hash"], current["dna"], timeout=TIMEOUT)
                if response:
                    done = True
                    break
            except requests.exceptions.Timeout:
                pass
            except:
                raise NetworkException
            sleep(0.1 * 2**i)

        if done:
            del upload_queue[0]
        else:
            raise NetworkException


def insert_genome(dna: str) -> None:
    genome = Genome(dna)

    if genome.hash() in genome_cache:
        return

    ehash = encrypt(genome.hash())
    edna = encrypt(dna)

    json = {"hash": ehash, "dna": edna}

    upload_queue.append(json)

    genome_cache[genome.hash()] = genome

    empty_queue()


if __name__ == "__main__":
    print(decrypt(encrypt("HelloWorld1")))
    rook_genome = "AHH HSH HAA CHA CHA CHA HHA SAS AAA AAA AAA".replace(
        " ", "")
    insert_genome(rook_genome)
