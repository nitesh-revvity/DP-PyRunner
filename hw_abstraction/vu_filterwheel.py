from devicepilot.pylog.pylogger import PyLogger
from config_enum  import filter_wheel_enum
from devicepilot.hw_abstraction.mover_ctrl import Mover
from devicepilot.urpc.moverfunctions import MoverFunctions

class VUFilterWheel(Mover):

    def __init__(self, hal_enum):
        super().__init__(hal_enum)
        self.endpoint: MoverFunctions = self.endpoint

    async def initialize_device(self):
        await super().initialize_device()


    async def select_position(self, descriptor_enum: str):
        """
        Selects a position on the filter wheel.
        :param descriptor_enum: The position to select.
        :return: no return value
        """
        PyLogger.logger.debug(f"Selecting position {descriptor_enum}")
        if descriptor_enum not in filter_wheel_enum.Positions.__members__:
            PyLogger.logger.error(f"Invalid position descriptor: {descriptor_enum}")
            return
        
        await self.move_to_named_position(filter_wheel_enum.Positions[descriptor_enum])
        PyLogger.logger.debug(f"Position {descriptor_enum} selected")

    async def goto_max_position(self):
        await self.move_to_named_position(filter_wheel_enum.Positions.Signal_max)

    async def move_to_filter(self, pos_index):
        """
        Moves the filter wheel to a specific position index.
        :param pos_index: The index of the position to move to.
        :return: no return value
        """
        PyLogger.logger.debug(f"Moving filter wheel to position index {pos_index}")
        if pos_index < 0:
            PyLogger.logger.error(f"Invalid position index: {pos_index}")
            return
        
        offset = self.get_config(filter_wheel_enum.GC_Params.filter_offset)
        filter_angle = self.get_config(filter_wheel_enum.GC_Params.filter_angle)
        name = self.get_config(filter_wheel_enum.FilterWheel.GCID)
        position = ((pos_index - 2) * filter_angle) + offset
        PyLogger.logger.info(f"set {name} to position {pos_index}: {position}°")
        await self.move(position)

    async def set_filter_by_wavelengh(self, wavelength : int):
        """
        Sets the filter wheel to a position based on the specified wavelength.
        :param wavelength: The wavelength to set the filter wheel to.
        :return: no return value
        """
        PyLogger.logger.debug(f"Setting filter wheel to wavelength {wavelength}")

        if wavelength is None:
            pos_index = 2
        elif wavelength < 360:
            pos_index = 3
        elif wavelength < 585:
            pos_index = 2
        elif wavelength <= 1000:
            pos_index = 1
        else:
            pos_index = 4

        await self.move_to_filter(pos_index=pos_index)

    async def get_max_position(self):
        """
        Gets the maximum position of the filter wheel.
        :return: The maximum position.
        """
        return self.get_config(filter_wheel_enum.Positions.Max)
    
    async def get_min_position(self):
        """
        Gets the minimum position of the filter wheel.
        :return: The minimum position.
        """ 
        return self.get_config(filter_wheel_enum.Positions.Min)
    
    async def get_sensors_status(self):
        """
        Gets the status of the sensors on the filter wheel.
        :return: The status of the sensors.
        """
        PyLogger.logger.debug("Getting filter wheel sensors status")
        second_light_barrier= await self.endpoint.get_digital_input(self.get_config(filter_wheel_enum.Sensors.SecondLightBarrier))
        home_sensor= await self.endpoint.get_digital_input(self.get_config(filter_wheel_enum.Sensors.Home))
        inside = (home_sensor == 1) and (second_light_barrier == 0)
        return ( home_sensor, second_light_barrier, inside)

        