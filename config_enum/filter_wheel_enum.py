from devicepilot.config_enum.config_enum_base import ConfigEnumBase
from devicepilot.config_enum import mover_enum

class Unit(ConfigEnumBase):
    GCID = ''
    CANID = ''


class Mover(mover_enum.Mover):
    pass


class Positions(mover_enum.Positions):
    Min = ''
    Max = ''
    Signal_max = ''



class GC_Params(ConfigEnumBase):
    pass


class Profile_Home(mover_enum.Profile):
    pass


class Profile_Operation(mover_enum.Profile):
    pass


class FI_Bottom(ConfigEnumBase):
    pass