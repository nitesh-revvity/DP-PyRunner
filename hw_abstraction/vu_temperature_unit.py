from devicepilot.hw_abstraction.temperature_ctrl import TemperatureControl

class TemperatureUnit(TemperatureControl):
    def __init__(self, hal_vu_enum):
        super().__init__( hal_vu_enum)

    async def initialize_device(self):
        """
        Initialize the temperature unit.
        """
        await super().initialize_device()
        # Additional initialization logic can be added here if needed.

    async def set_target_temperature(self, target_temperature):
        """
        Set the target temperature for the unit.
        """
        await self.set_pid_setpoint(target_temperature)

    async def get_temperature_values(self):
        temp = await self.get_pid_feedback_value()
        output = await self.get_output_workload()
        setpoint = await self.get_pid_setpoint()
        #offset = await self.get_offset_value()
        unit_name = self.name
        temp_dict = {"Unit": unit_name,
                     "Temperature": temp,
                     "Workload": output,
                     "Setpoint": setpoint,
                     #"Offset": offset
                     }

        return temp_dict
    
