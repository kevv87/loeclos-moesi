from enum import Enum

class Events(Enum):
    PROCESSOR_CREATION              = 1  

    GENERATED_CALC_OPERATION        = 2
    GENERATED_WRITE_OPERATION       = 3
    GENERATED_READ_OPERATION        = 4
    GENERATED_RESPONSE_OPERATION    = 5

    CACHE_READ                      = 6
    CACHE_HIT                       = 7
    CACHE_MISS                      = 8

    CACHE_REQUESTING_VALUE_BUS      = 9

    CACHE_GIVES_RESPONSE            = 10
    RETRIEVING_FROM_MEMORY          = 11

    REPLACING_BLOCK                 = 12
    WRITING_BLOCK                   = 13
    UPDATING_BLOCK                  = 14

    WRITEBACK                       = 15

class Objects(Enum):
    MEMORY      = "memory"
    CACHE       = "cache"
    PROCESSOR   = "processor"
    OPERATION   = "operation"

