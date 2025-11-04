from devicepilot.config_enum.config_enum_base import ConfigEnumBase


class Unit(ConfigEnumBase):
    GCID = ''
    CANID = ''
    DisplayName = ''
    Description = ''
    

class Fan(ConfigEnumBase):
    
    SpeedMeasWindow_ms = ''
    Enable = ''
    Channel = ''
    RevolutionPerPulse = ''
    RevolutionPerMinute = ''
    MaxDeviation_perc = ''
    MinSpeed_perc = ''
    IdleSpeed_perc = ''
    MaxSpeed_perc = ''


class GC_Params(ConfigEnumBase):
    pass
