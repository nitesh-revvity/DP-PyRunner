from devicepilot.config_enum.config_enum_base import ConfigEnumBase


class Events(ConfigEnumBase):
    Rising = ''
    Falling = ''
    Both = ''

class Sensors(ConfigEnumBase):
    CanNode = ''
    DigitalInput  = ''