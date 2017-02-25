from enum import Enum

class BaseEnum(Enum):

    @classmethod
    def from_string(cls, str):
        return getattr(cls, str.upper(), None)

class Tariff(BaseEnum):
    PAY_MONTHLY = 1
    PAY_AND_GO = 2

class CallType(BaseEnum):
    LANDLINE = "Landline"
    MOBILE = "Mobiles"
    TEXT = "Cost per text message"

    