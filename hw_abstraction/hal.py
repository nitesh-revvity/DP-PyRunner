from devicepilot.hw_abstraction.hal import HALBase
from devicepilot.hw_abstraction.node_ctrl import Node
from devicepilot.hw_abstraction.mover_ctrl import Mover
from devicepilot.hw_abstraction.temperature_ctrl import TemperatureControl
from devicepilot.hw_abstraction.dual_mover_ctrl import DualMover

from hw_abstraction.light_switch_emission import LightSwitchEmission
from hw_abstraction.light_switch_excitation import LightSwitchExcitation
from hw_abstraction.monochromator_emission import MonochromatorEmission
from hw_abstraction.monochromator_excitation import MonochromatorExcitation
from hw_abstraction.filter_wheel_pmt import FilterWheelPMT
from hw_abstraction.filter_wheel_flashlamp import FilterWheelFlashLamp
from hw_abstraction.upper_measurehead import UpperMeasureHead
from hw_abstraction.scan_table import ScanTable
from hw_abstraction.vu_fan import Fan
from hw_abstraction.vu_temperature_unit import TemperatureUnit


from config_enum import hal_enum
from hw_abstraction.plate_door_sensor import PlateDoorSensor
#from devicepilot.hw_abstraction.measurement_unit_ctrl import MeasurementUnit
from devicepilot.pylog.pylogger import PyLogger

from config_enum import platedoor_sensor_enum

class MC6(Node):
    def __init__(self, hal_vu_enum):
        super().__init__( hal_vu_enum)
    
    async def get_sensor_input(self):
        """Get the current state of the plate door sensor.
        use mc6 digital input
        """
        sensor_state = await self.endpoint.get_digital_input(self.get_config(platedoor_sensor_enum.Sensors.DigitalInput))
        return sensor_state



class HAL(HALBase):
    def __init__(self):
        HALBase.__init__(self)

        self.mainboard_node             = self.hw_controller_factory( Node,     hal_enum.HAL.Mainboard)
        self.mc6 = self.hw_controller_factory(MC6, hal_enum.HAL.MC6 )
        self.eefnode = self.hw_controller_factory(Node, hal_enum.HAL.EEFNode )

        #self.plate_door                 = self.hw_controller_factory( PlateDoor, hal_enum.HAL.PlateDoor )
        #self.scan_table:DualMover     = self.hw_controller_factory( ScanTable, hal_enum.HAL.ScanTable )
        self.light_switch_excitation = self.hw_controller_factory( LightSwitchEmission, hal_enum.HAL.LightSwitchEmission )
        self.light_switch_emission = self.hw_controller_factory( LightSwitchExcitation, hal_enum.HAL.LightSwitchExcitation )
        self.monochromator_emission = self.hw_controller_factory( MonochromatorEmission, hal_enum.HAL.MonochromatorEmissionMover )
        self.monochromator_excitation = self.hw_controller_factory( MonochromatorExcitation, hal_enum.HAL.MonochromatorExcitationMover )
        self.filter_wheel_pmt = self.hw_controller_factory( FilterWheelPMT, hal_enum.HAL.FilterWheelPMT )
        self.filter_wheel_flashlamp = self.hw_controller_factory( FilterWheelFlashLamp, hal_enum.HAL.FilterWheelFlashLamp )
        self.upper_measure_head = self.hw_controller_factory( UpperMeasureHead, hal_enum.HAL.UpperMeasureHead )
        
        # Controlled Fan Units
        self.air_ventilation_fan = self.hw_controller_factory( Fan, hal_enum.HAL.AirVentilationFan )
        self.groundplate_fan = self.hw_controller_factory( Fan, hal_enum.HAL.GroundplateFan )
        self.flashlamp_fan = self.hw_controller_factory( Fan, hal_enum.HAL.FlashlampFan )

        # Heating Units
        self.lower_heating = self.hw_controller_factory( TemperatureUnit, hal_enum.HAL.LowerHeating )
        self.upper_heating = self.hw_controller_factory( TemperatureUnit, hal_enum.HAL.UpperHeating )
        self.pmtch1_cooling = self.hw_controller_factory( TemperatureUnit, hal_enum.HAL.PMTch1Cooling ) 

        self.plate_door_sensor = self.hw_controller_factory( PlateDoorSensor, hal_enum.HAL.PlateDoorSensor )


        # self.measurement_unit = self.hw_controller_factory( MeasurementUnit, hal_enum.HAL.MeasurementUnit )


