from devicepilot.config_enum.config_enum_base import ConfigEnumBase
from devicepilot.config_enum import dualmover_enum

class Unit(ConfigEnumBase):
    GCID = ''
    CANID = ''


class GC_Params(ConfigEnumBase):
    FI_Top_TopLeftCorner = ''


class Mover(ConfigEnumBase):
    pass


class Positions(dualmover_enum.Positions):
    pass


class Profile_Home(dualmover_enum.Profile):
    pass


class Profile_Operation(dualmover_enum.Profile):
    pass


class Profile_Test(dualmover_enum.Profile):
    pass

