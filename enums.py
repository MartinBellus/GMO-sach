from enum import StrEnum, Enum, auto, EnumMeta

class ExtendedEnum(StrEnum):
    @classmethod
    def __contains__(cls, other):
        return other in cls.list()
    
class MyEnumMeta(EnumMeta): 
    def __contains__(cls, item): 
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True

class control_codons(StrEnum, metaclass=MyEnumMeta):
    SEPARATOR_BEGIN = "AHH"
    SEPARATOR_END = "HHA"

class debuff_codons(StrEnum, metaclass=MyEnumMeta):
    TEST_DEBUFF = "HAA"

class player_codons(StrEnum, metaclass=MyEnumMeta):
    OPPONENT = "HSH"

class players(Enum):
    ME = auto()
    OPPONENT = auto()
    
class colors(Enum):
    BLACK = auto()
    WHITE = auto()

class which_piece(StrEnum, metaclass=MyEnumMeta):
    MINE = "A"
    OPPONENTS = "S"
    NONE = "C"