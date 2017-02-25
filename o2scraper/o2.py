from enum import Enum

class Tariff(Enum):
    PAY_MONTHLY = 1
    PAY_AND_GO = 2

class CallType(ENUM):
    LANDLINE = 1
    MOBILE = 2
    TEXT_MESSAGE = 3