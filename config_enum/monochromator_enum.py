from devicepilot.config_enum.config_enum_base import ConfigEnumBase
from devicepilot.config_enum import mover_enum

class Unit(ConfigEnumBase):
    GCID = ''
    CANID = ''
    Min_WaveLength = ''
    Max_WaveLength = ''


class Mover(mover_enum.Mover):
    pass


class Positions(mover_enum.Positions):
    pos_zero_order = ''
    pos_at_365nm = ''
    pos_at_488nm = ''
    pos_at_635nm = ''
    pos_at_785nm = ''



class GC_Params(ConfigEnumBase):
    pass


class Profile_Home(mover_enum.Profile):
    pass


class Profile_Operation(mover_enum.Profile):
    pass


class FI_Bottom(ConfigEnumBase):
    pass