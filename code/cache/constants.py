from enum import Enum
from code.processors.constants import PROCESSOR_ACTION_SECONDS

CACHE_ACCESS_SECONDS = PROCESSOR_ACTION_SECONDS * 2

class MoesiStates(Enum):
    M = "M"
    O = "O"
    E = "E"
    S = "S"
    I = "I"

class MoesiEvents(Enum):
    SELF_READ = 0
    SELF_WRITE = 1
    OTHERS_READ = 2
    OTHERS_WRITE = 3
    EXCLUSIVE_READ = 4
