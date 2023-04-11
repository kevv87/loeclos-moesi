from code.cache.constants import *

moesiStateMachine = {
    MoesiStates.I: {
        MoesiEvents.SELF_WRITE: MoesiStates.M,
        MoesiEvents.SELF_READ: MoesiStates.S,
        MoesiEvents.OTHERS_WRITE: MoesiStates.I,
        MoesiEvents.OTHERS_READ: MoesiStates.I,
        MoesiEvents.EXCLUSIVE_READ: MoesiStates.E
    },
    MoesiStates.M: {
        MoesiEvents.SELF_WRITE: MoesiStates.M,
        MoesiEvents.SELF_READ: MoesiStates.M,
        MoesiEvents.OTHERS_WRITE: MoesiStates.I,
        MoesiEvents.OTHERS_READ: MoesiStates.O,
        MoesiEvents.EXCLUSIVE_READ: MoesiStates.M
    },
    MoesiStates.S: {
        MoesiEvents.SELF_WRITE: MoesiStates.M,
        MoesiEvents.SELF_READ: MoesiStates.S,
        MoesiEvents.OTHERS_WRITE: MoesiStates.I,
        MoesiEvents.OTHERS_READ: MoesiStates.S,
        MoesiEvents.EXCLUSIVE_READ: MoesiStates.S
    },
    MoesiStates.E: {
        MoesiEvents.SELF_WRITE: MoesiStates.M,
        MoesiEvents.SELF_READ: MoesiStates.E,
        MoesiEvents.OTHERS_WRITE: MoesiStates.I,
        MoesiEvents.OTHERS_READ: MoesiStates.S,
        MoesiEvents.EXCLUSIVE_READ: MoesiStates.E
    },
    MoesiStates.O: {
        MoesiEvents.SELF_WRITE: MoesiStates.M,
        MoesiEvents.SELF_READ: MoesiStates.O,
        MoesiEvents.OTHERS_WRITE: MoesiStates.I,
        MoesiEvents.OTHERS_READ: MoesiStates.O,
        MoesiEvents.EXCLUSIVE_READ: MoesiStates.O
    }
}

class Moesi():
    def compute_next_state(self, current_state, action):
        return moesiStateMachine[current_state][action]
