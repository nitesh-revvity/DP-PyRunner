from devicepilot.hw_abstraction.node_ctrl import Node
from config_enum import platedoor_sensor_enum
from devicepilot.urpc.nodefunctions import NodeFunctions
from devicepilot.urpc_sim.nodefunctions_sim import NodeFunctionsSim

class PlateDoorSensor(Node):
    """Placeholder class for Plate Door Sensor hardware abstraction layer."""
    def __init__(self, hal_vu_enum):
        super().__init__(hal_vu_enum)

        CANID = self.get_config(platedoor_sensor_enum.Sensors.CanNode)
        self.digital_input = self.get_config(platedoor_sensor_enum.Sensors.DigitalInput)
        self.events = self.get_config(platedoor_sensor_enum.Events.Both)


    def initialize_device(self):
        super().initialize_device()


    async def get_sensor_input(self):
        """Get the current state of the plate door sensor.
        use mc6 digital input
        """
        sensor_state = await self.endpoint.get_digital_input(self.get_config(platedoor_sensor_enum.Sensors.DigitalInput))
        return sensor_state
    
    