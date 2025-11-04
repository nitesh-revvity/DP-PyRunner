import devicepilot.config_enum.hal_enum  as hal_enum_base
from devicepilot.config_enum.config_enum_base import ConfigEnumBase


class HAL(hal_enum_base.HAL):
    Mainboard = ''
    Mover1=''
    NodeApplication = ''
    LightSwitchEmission=''
    LightSwitchExcitation=''
    MonochromatorEmissionMover=''
    MonochromatorExcitationMover=''
    FilterWheelPMT = ''
    FilterWheelFlashLamp= ''
    UpperMeasureHead=''
    #MeasurementUnit=''
    ScanTable = ''
    NodeApplication = ''
    MC6 = ''
    EEFNode = ''
    
    # Controlled Fan Units
    AirVentilationFan = ''
    GroundplateFan = ''
    FlashlampFan = ''

    # Heating Units
    LowerHeating = ''
    UpperHeating = ''
    PMTch1Cooling = ''

    # Sensors
    PlateDoorSensor = ''
    