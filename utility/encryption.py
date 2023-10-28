ENCRYPTION_KEY = "1gSD89IsdfjIie4gs454G2werg3W23gw3GW8WGwg5wG8sU4Euer3434urt6u4s64g8KHGWERg64sfg"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-"
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