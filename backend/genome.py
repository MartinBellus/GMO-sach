from utility.constants import *
from utility.enums import *
from utility.vector import Vector, inside_chessboard
from backend.move_descriptor import MoveDescriptor
from backend.genome_cache import fetch_dna, upload_dna
from utility.exceptions import InvalidGenomeException, OutOfCodons
from copy import copy
import hashlib
import re
import random


def remove_blank(s: str) -> str:
    return re.sub(r'\s', '', s)


def genome_assert(condition: bool, message: str = "Invalid genome."):
    if not condition:
        raise InvalidGenomeException(message)


def ternary_to_int(ternary: str) -> int:
    genome_assert(all(c in "SACH" for c in ternary),
                  "Ternary must only contain S, A, C, and H.")
    number_map = {"A": "0", "S": "1", "C": "2"}
    numbers = "".join([number_map[c] for c in ternary])
    return int(numbers, 3)


class DnaStream:
    # class for storing the DNA and extracting it one by one
    # makes invalid genome easier to detect
    def __init__(self, dna: str):
        genome_assert(len(dna) %
                      3 == 0, "Length of DNA must be a multiple of 3.")
        genome_assert(all(c in "SACH" for c in dna),
                      "DNA must only contain S, A, C, and H.")
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

    def add_codon(self, codon: str):
        genome_assert(len(codon) == 3, "Codon must be 3 characters long.")
        genome_assert(all(c in "SACH" for c in codon),
                      "Codon must only contain S, A, C, and H.")
        self.dna += codon
        self.length += 1
        self.codons.append(codon)

    def reset(self):
        self.next_codon = 0

    def empty(self):
        return self.next_codon == self.length

    def get_string(self):
        return self.dna


class Movement:
    def __init__(self, distance: int, coloring: bool):
        self.distance = distance
        self.coloring = coloring


class Spirulateral:
    def __init__(self, codons: DnaStream):
        # DNA stream
        self.codons = codons

        # who will own pieces on current and next tile after a move
        self.owner_on_current = Players.OPPONENT
        self.owner_on_next = Players.OPPONENT

        # which pieces will be copied into current and next tile after a move depending on what lies on the target tile
        self.on_opponent_capture: tuple[WhosePiece, WhosePiece] = None
        self.on_own_capture: tuple[WhosePiece, WhosePiece] = None
        self.on_no_capture: tuple[WhosePiece, WhosePiece] = None

        # the debuffs that this spirulateral has
        self.debuffs = set()

        # the parts of the spirulateral
        self.parts: list[Movement] = list()

        self.parse_spirulateral()

    def parse_spirulateral(self):
        genome_assert(not self.codons.empty(),
                      "Spirulateral must have at least one codon.")
        genome_assert(self.codons.get_codon() == ControlCodons.SEPARATOR_BEGIN,
                      f"Spirulateral must start with {ControlCodons.SEPARATOR_BEGIN}.")

        # process separator

        # get owner_on_current

        codon = self.codons.get_codon()

        if codon == PlayerCodons.OPPONENT:
            self.owner_on_current = Players.OPPONENT
        elif codon in DebuffCodons:
            genome_assert(codon not in self.debuffs,
                          f"Debuff {codon} cannot be applied twice.")
            self.debuffs.add(codon)
            self.owner_on_current = Players.ME
        else:
            genome_assert(False, f"Invalid codon {codon} in spirulateral.")

        # get owner_on_next
        codon = self.codons.get_codon()

        if codon == PlayerCodons.OPPONENT:
            self.owner_on_next = Players.OPPONENT
        elif codon in DebuffCodons:
            genome_assert(codon not in self.debuffs,
                          f"Debuff {codon} cannot be applied twice.")
            self.debuffs.add(codon)
            self.owner_on_next = Players.ME
        else:
            genome_assert(False, f"Invalid codon {codon} in spirulateral.")

        # process capture codons

        self.on_own_capture = self.parse_capture_codon()
        self.on_opponent_capture = self.parse_capture_codon()
        self.on_no_capture = self.parse_capture_codon()

        genome_assert(self.codons.get_codon() == ControlCodons.SEPARATOR_END,
                      f"Separator must end with {ControlCodons.SEPARATOR_END}.")

        # process spirulateral body

        while self.codons.has_next():
            self.parts.append(self.parse_movement())

        genome_assert(len(self.parts) <= 4,
                      "Spirulateral must have at most 4 parts.")

    def parse_capture_codon(self) -> tuple[WhosePiece, WhosePiece] | None:
        codon = self.codons.get_codon()
        if codon == MOVE_IMPOSSIBLE_CODON:
            return None
        genome_assert(codon[1] == "H",
                      "Middle character of capture codon must be H.")
        genome_assert(codon[0] in WhosePiece,
                      f"First character of capture codon must be in {WhosePiece}.")
        genome_assert(codon[2] in WhosePiece,
                      f"Third character of capture codon must be in {WhosePiece}.")

        return (codon[0], codon[2])

    def parse_movement(self):
        codon = self.codons.get_codon()

        genome_assert(all(c in "SAC" for c in codon),
                      "Codon must only contain S, A, C.")

        coloring = codon[0] == "S"

        dist = ternary_to_int(codon[1:]) % (3 if coloring else 5)

        if codon[0] == 'A':
            dist = 0

        return Movement(dist, coloring)

    def get_moves(self, chessboard: dict[Vector, Players], position: Vector, debuffs: set[DebuffCodons]) -> list[MoveDescriptor]:

        # in one direction of rotation
        ans: [MoveDescriptor] = []
        for starting_direction in range(4):
            moves = self.generate_moves_in_direction(
                chessboard, position, starting_direction, 1, debuffs)
            ans.extend(moves)

        # and the other
        for starting_direction in range(4):
            moves = self.generate_moves_in_direction(
                chessboard, position, starting_direction, -1, debuffs)
            ans.extend(moves)

        return ans

    def generate_moves_in_direction(self, chessboard: dict[Vector, Players], position: Vector, direction: int, delta: int, debuffs: set[DebuffCodons]) -> list[MoveDescriptor]:
        moves: [MoveDescriptor] = []

        direction_vectors = [Vector(0, 1), Vector(
            1, 0), Vector(0, -1), Vector(-1, 0)]

        visited = set()
        i = 0
        current_position = position
        while 1:
            # move according to the current part of the spirulateral
            current_position += direction_vectors[direction] * \
                self.parts[i].distance

            if DebuffCodons.NO_TELEPORTING_BETWEEN_SIDES not in debuffs:
                current_position.x %= BOARD_X

            # make sure not to go out of bounds
            if not inside_chessboard(current_position):
                break

            # make sure we don't get stuck in a cycle
            if (current_position, direction, i) in visited:
                break
            visited.add((current_position, direction, i))

            # maybe color the tile if the move is coloring
            if self.parts[i].coloring:
                descriptor = self.make_move_descriptor(
                    chessboard, current_position, position)
                if descriptor is not None:
                    moves.append(descriptor)

            # when we hit a piece, the spirulateral ends but only if the move is coloring
            if current_position in chessboard and self.parts[i].coloring:
                break

            # go to the next part of the spirulateral
            i = (i+1) % len(self.parts)
            # direction goes to the next/previous in rotation depending on delta
            direction = (direction+delta) % 4

            if DebuffCodons.SPIRULATERAL_ONLY_REPEATS_ONCE in self.debuffs and i == 0:
                break
        return moves

    def make_move_descriptor(self, chessboard, current_pos, original_pos) -> MoveDescriptor:
        which_to_copy = {Players.NONE: self.on_no_capture, Players.ME: self.on_own_capture,
                         Players.OPPONENT: self.on_opponent_capture}

        whos_there = chessboard.get(current_pos, Players.NONE)

        copied = which_to_copy[whos_there]

        if copied is None:
            return None

        here = (copied[0], self.owner_on_current)
        there = (copied[1], self.owner_on_next)

        return MoveDescriptor(original_pos, current_pos, here, there)

    def get_debuffs(self):
        return copy(self.debuffs)


class Genome:
    def __init__(self, dna: str):
        self.raw_dna: str = remove_blank(dna)
        self.dna = DnaStream(self.raw_dna)
        self.spirulaterals: list[Spirulateral] = []
        self.debuffs = set()
        self.parse_dna()
        self.save()

    def parse_dna(self) -> None:
        while self.dna.has_next():
            self.parse_spirulateral()
        for i in self.spirulaterals:
            i.debuffs = self.debuffs.copy()

    def parse_spirulateral(self) -> None:
        if not self.dna.has_next():
            return

        codon = self.dna.peek_codon()
        genome_assert(codon == ControlCodons.SEPARATOR_BEGIN,
                      f"Separator must start with {ControlCodons.SEPARATOR_BEGIN}.")

        spirulateral_dna = DnaStream("")

        while self.dna.has_next():
            codon = self.dna.peek_codon()
            if codon == ControlCodons.SEPARATOR_BEGIN and not spirulateral_dna.empty():
                break
            spirulateral_dna.add_codon(self.dna.get_codon())

        spirulateral = Spirulateral(spirulateral_dna)
        self.spirulaterals.append(spirulateral)

        debuffs = spirulateral.get_debuffs()
        for debuff in debuffs:
            genome_assert(debuff not in self.debuffs,
                          f"Debuff {debuff} cannot be applied twice.")
            self.debuffs.add(debuff)

    def hash(self) -> str:
        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
        hsh = hashlib.sha256(self.dna.get_string().encode()).digest()[:6]
        res = ""
        for i in hsh:
            res += ALPHABET[i % len(ALPHABET)]
        return res

    def get_moves(self, chessboard: dict[Vector, Players], position: Vector) -> list[MoveDescriptor]:
        moves: [MoveDescriptor] = []
        for spirulateral in self.spirulaterals:
            moves.extend(spirulateral.get_moves(
                chessboard, position, self.debuffs))

        # deduplicate moves

        seen = set()

        ans: [MoveDescriptor] = []

        for move in moves:
            if move.to_position in seen:
                continue
            seen.add(move.to_position)
            ans.append(move)

        return ans

    @classmethod
    def from_hash(cls, hash: str):
        return cls(fetch_dna(hash))

    def save(self):
        upload_dna(self.hash(), self.dna.get_string())

    def get_debuffs(self):
        return copy(self.debuffs)

    def mutate(self):
        ATTEMPTS = 20
        EDITS = 1

        for _ in range(ATTEMPTS):
            new_dna = self.dna.get_string()
            for _ in range(EDITS):
                index = random.randint(0, len(new_dna)-1)
                new_dna = new_dna[:index] + \
                    random.choice([i for i in "SACH" if i !=
                                  new_dna[index]]) + new_dna[index+1:]
            try:
                return Genome(new_dna)
            except InvalidGenomeException:
                pass
        return self


# TESTING
if __name__ == "__main__":
    rook_genome = "AHH HSH HAA CHA CHA CHA HHA SAS AAA AAA AAA".replace(
        " ", "")
    genome = Genome(rook_genome)
    pass
