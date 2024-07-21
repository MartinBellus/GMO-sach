from enum import StrEnum, Enum, auto, EnumMeta


class ExtendedEnum(StrEnum):
    @classmethod
    def __contains__(cls, other):
        return other in cls.list()

# fancy metaclass to allow in operator on enums


class MyEnumMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class ControlCodons(StrEnum, metaclass=MyEnumMeta):
    SEPARATOR_BEGIN = "AHH"
    SEPARATOR_END = "HHA"


class DebuffCodons(StrEnum, metaclass=MyEnumMeta):
    FORWARD_ONLY = "HAS"
    SPIRULATERAL_ONLY_REPEATS_ONCE = "HAC"
    NO_TELEPORTING_BETWEEN_SIDES = "HAA"
    ONLY_CAN_COLOR_SAME_COLOR = "HCS"
    ONLY_CAN_COLOR_DIFFERENT_COLOR = "HCA"
    ONLY_CAN_COLOR_NEIGHBOURS = "HSS"
    GAME_FREEZES_ON_MOVE = "HSC"
    RANDOM_MUTATION = "HCC"
    RANDOM_MOVE_DEVIATION = "HSA"


class PlayerCodons(StrEnum, metaclass=MyEnumMeta):
    OPPONENT = "HSH"


class Players(Enum):
    ME = auto()
    OPPONENT = auto()
    NONE = auto()


class Colors(Enum):
    BLACK = auto()
    WHITE = auto()


class WhosePieceEnum(StrEnum, metaclass=MyEnumMeta):
    MINE = "A"
    OPPONENTS = "S"
    NONE = "C"


class GameStatus(Enum):
    BLACK_WON = auto()
    WHITE_WON = auto()
    DRAW = auto()
    IN_PROGRESS = auto()
    NOT_STARTED = auto()
    START_GAME = auto()
    LAB = auto()


GameOverStatuses = (GameStatus.BLACK_WON,
                    GameStatus.WHITE_WON, GameStatus.DRAW)

MOVE_IMPOSSIBLE_CODON = "HHH"
