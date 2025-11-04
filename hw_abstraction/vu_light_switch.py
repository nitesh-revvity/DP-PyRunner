from devicepilot.pylog.pylogger import PyLogger
from config_enum  import light_switch_enum
from devicepilot.hw_abstraction.mover_ctrl import Mover
from devicepilot.urpc.moverfunctions import MoverFunctions

class VULightSwitch(Mover):
    """
    Class to represent ExcitationLight Selector device.
    The device has one mover to select to different lights
    """
    def __init__(self, hal_enum):
        super().__init__(hal_enum)
        self.endpoint: MoverFunctions = self.endpoint

    async def initialize_device(self):
        """
        Initializes the mover
        :return: no return value
        """
        PyLogger.logger.debug("ExcitationLightSelector InitializeDevice")
        await super().initialize_device()

    async def goto_fi_top_position(self):
        await self.move_to_named_position(light_switch_enum.Positions.FI_Top)

    async def goto_fi_bottom_position(self):
        await self.move_to_named_position(light_switch_enum.FI_Bottom.FI_Bottom)

    async def goto_abs_position(self):
        await self.move_to_named_position(light_switch_enum.Positions.ABS)

    async def select_position(self, descriptor_enum):
        pass

    async def get_max_position(self):
        return self.get_config(light_switch_enum.Positions.Max)

    async def get_min_position(self):
        return self.get_config(light_switch_enum.Positions.Min)
    
    async def goto_position(self, position):
        """
        Moves the light switch to a specific position.
        :param position: The position to move to.
        :return: no return value
        """
        PyLogger.logger.debug(f"Moving light switch to position {position}")
        await self.move(position)
        PyLogger.logger.debug(f"Light switch moved to position {position}")