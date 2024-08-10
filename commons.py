from enum import Enum


class ExternalData(Enum):
    SP_500 = "%5EGSPC"
    PPL = "ppl"
    VWRLL = "VWRL.L"
    NASDAQ100 = "CNX1.L"


class T212Periods(Enum):
    LAST_DAY = "LAST_DAY"
    ALL = "ALL"
