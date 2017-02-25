from enum import Enum

class Tariff(Enum):
    PAY_MONTHLY = 1
    PAY_AND_GO = 2

class CallType(Enum):
    LANDLINE = "Landline"
    MOBILE = "Mobiles"
    TEXT_MESSAGE = "Cost per text message"