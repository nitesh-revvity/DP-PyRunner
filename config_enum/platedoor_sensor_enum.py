from devicepilot.config_enum.config_enum_base import ConfigEnumBase

class Unit(ConfigEnumBase):
    CANID = ''


class GC_Params(ConfigEnumBase):
    Dummy = ''


class Events(ConfigEnumBase):
    Rising = ''
    Falling = ''
    Both = ''

class Sensors(ConfigEnumBase):
    CanNode = ''
    DigitalInput  = ''


