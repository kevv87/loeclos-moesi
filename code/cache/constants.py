from enum import Enum

class MoesiStates(Enum):
    M = 0
    O = 1
    E = 2
    S = 3
    I = 4

class MoesiEvents(Enum):
    SELF_READ = 0
    SELF_WRITE = 1
    OTHERS_READ = 2
    OTHERS_WRITE = 3
    EXCLUSIVE_READ = 4
