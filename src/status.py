from enum import Enum

class Status(Enum):

    OK = 1
    CORRECTABLE_ERROR = 2
    UNCORRECTABLE_ERROR = 3