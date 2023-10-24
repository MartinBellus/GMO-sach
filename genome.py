from enums import *
import hashlib

class InvalidGenomeException(Exception): pass
class OutOfCodons(InvalidGenomeException): pass

def genome_assert(condition:bool, message:str="Invalid genome."):
    if not condition:
        raise InvalidGenomeException(message)

def ternary_to_int(ternary:str) -> int:
    genome_assert(all(c in "SACH" for c in ternary), "Ternary must only contain S, A, C, and H.")
    number_map={"A":"0", "S":"1", "C":"2"}
    numbers = "".join([number_map[c] for c in ternary])
    return int(numbers, 3)

class DnaStream:
    def __init__(self, dna:str):
        genome_assert(len(dna) % 3 == 0, "Length of DNA must be a multiple of 3.")
        genome_assert(all(c in "SACH" for c in dna), "DNA must only contain S, A, C, and H.")
        self.dna = dna
        self.length = len(dna)//3 
        self.codons = [self.dna[i:i+3] for i in range(0, len(self.dna), 3)]
        self.next_codon = 0

    def get_codon(self) -> str:
        if self.next_codon >= self.length:
            raise OutOfCodons

        result = self.codons[self.next_codon]
        self.next_codon += 1
        return result

    def has_next(self):
        return self.next_codon < self.length
    
    def peek_codon(self):
        if self.next_codon >= self.length:
            raise OutOfCodons

        return self.codons[self.next_codon]
    
    def add_codon(self, codon:str):
        genome_assert(len(codon) == 3, "Codon must be 3 characters long.")
        genome_assert(all(c in "SACH" for c in codon), "Codon must only contain S, A, C, and H.")
        self.dna += codon
        self.length += 1
        self.codons.append(codon)
        
    def reset(self):
        self.next_codon = 0
        
    def empty(self):
        return self.next_codon == self.length

class Movement:
    def __init__(self, distance:int, coloring:bool):
        self.distance = distance
        self.coloring = coloring

class Spirulateral:
    def __init__(self, codons:DnaStream):
        self.codons = codons
        self.next_codon = 0
        self.owner_on_current = players.OPPONENT
        self.owner_on_next = players.OPPONENT
        self.on_opponent_capture : tuple[int, int] = None
        self.on_own_capture : tuple[int, int] = None
        self.on_no_capture : tuple[int, int] = None
        self.debuffs = []
        self.directions:list[Movement] = []

        
        self.parse_spirulateral()
    
    def parse_spirulateral(self):
        genome_assert(not self.codons.empty(), "Spirulateral must have at least one codon.")
        genome_assert(self.codons.get_codon() == control_codons.SEPARATOR_BEGIN, f"Spirulateral must start with {control_codons.SEPARATOR_BEGIN}.")
        
        #process separator

        #get owner_on_current

        codon=self.codons.get_codon()

        if codon == player_codons.OPPONENT:
            self.owner_on_current = players.OPPONENT
        elif codon in debuff_codons:
            self.debuffs.append(codon)
            self.owner_on_current = players.ME
        else:
            genome_assert(False, f"Invalid codon {codon} in spirulateral.")
        
        #get owner_on_next
        codon = self.codons.get_codon()

        if codon == player_codons.OPPONENT:
            self.owner_on_next = players.OPPONENT
        elif codon in debuff_codons:
            self.debuffs.append(codon)
            self.owner_on_next = players.ME
        else:
            genome_assert(False, f"Invalid codon {codon} in spirulateral.")

        #TODO: process debuffs

        #process capture codons

        self.on_own_capture = self.parse_capture_codon()
        self.on_opponent_capture = self.parse_capture_codon()
        self.on_no_capture = self.parse_capture_codon()
        
        genome_assert(self.codons.get_codon() == control_codons.SEPARATOR_END, f"Separator must end with {control_codons.SEPARATOR_END}.")
        
        #process spirulateral body
        
        while self.codons.has_next():
            self.directions.append(self.parse_movement())
    
    def parse_capture_codon(self) -> tuple[int, int]:
        codon = self.codons.get_codon()
        genome_assert(codon[1] == "H", "Middle character of capture codon must be H.")
        genome_assert(codon[0] in which_piece, f"First character of capture codon must be in {which_piece}.")
        genome_assert(codon[2] in which_piece, f"Third character of capture codon must be in {which_piece}.")
        
        return (codon[0], codon[2])
    
    def parse_movement(self):
        codon = self.codons.get_codon()

        coloring = codon[0] == "S"
        
        dist = ternary_to_int(codon[1:]) % 5
        
        return Movement(dist, coloring)

    def get_string(self):
        return self.codons.dna


class Genome:
    def __init__(self, dna:str):
        self.dna=DnaStream(dna)
        self.spirulaterals : list[Spirulateral] = []
        self.parse_dna()
    
    def parse_dna(self) -> None:
        while self.dna.has_next():
            self.parse_spirulateral()
    
    def parse_spirulateral(self) -> None:
        if not self.dna.has_next():
            return
        
        codon = self.dna.peek_codon()
        genome_assert(codon == control_codons.SEPARATOR_BEGIN, f"Separator must start with {control_codons.SEPARATOR_BEGIN}.")
        
        spirulateral_dna = DnaStream("")
        
        while self.dna.has_next():
            codon = self.dna.peek_codon()
            if codon == control_codons.SEPARATOR_BEGIN and not spirulateral_dna.empty():
                break
            spirulateral_dna.add_codon(self.dna.get_codon())
        
        self.spirulaterals.append(Spirulateral(spirulateral_dna))
    
    def hash(self) -> str:
        return hashlib.sha256(self.dna.get_string().encode()).hexdigest()[:6]
    

##TESTING
if __name__ == "__main__":
    rook_genome="AHH HSH HAA CHA CHA CHA HHA SAS AAA AAA AAA".replace(" ", "")
    genome = Genome(rook_genome)
    pass
    