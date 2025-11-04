from devicepilot.config_enum.config_enum_base import ConfigEnumBase
from devicepilot.config_enum import mover_enum


class Unit(ConfigEnumBase):
    SSWID=''
    CANID = ''


class GC_Params(ConfigEnumBase):
    Dummy = ''


class Positions(mover_enum.Positions):
    FI_Top = ''
    ABS = ''


class Profile_Home(mover_enum.Profile):
    pass


class Profile_Operation(mover_enum.Profile):
    pass


class Profile_Test(mover_enum.Profile):
    pass

class FI_Bottom(mover_enum.Positions):
    FI_Bottom = ''