from devicepilot.hw_abstraction.fan_ctrl import FanControl
from config_enum import fan_control_enum
from devicepilot.py_pli.pylib import GlobalVar


class Fan(FanControl):
    def __init__(self, hal_vu_enum):
        super().__init__( hal_vu_enum)

        self.unit_enable = self.get_config(fan_control_enum.Fan.Enable)
        self.unit_channel = self.get_config(fan_control_enum.Fan.Channel)
        self.unit_scale = self.get_config(fan_control_enum.Fan.RevolutionPerPulse)
        self.fan_speed_max = self.get_config(fan_control_enum.Fan.MaxSpeed_perc)
        self.fan_speed_idle = self.get_config(fan_control_enum.Fan.IdleSpeed_perc)
        self.fan_speed_min = self.get_config(fan_control_enum.Fan.MinSpeed_perc)
        self.revolution_per_minute = self.get_config(fan_control_enum.Fan.RevolutionPerMinute)
        self.max_deviation = self.get_config(fan_control_enum.Fan.MaxDeviation_perc)
        self.used_fan_speed = []
        

        if isinstance(self.unit_channel, int):
            self.unit_channel = [self.unit_channel]
            self.fan_speed_idle = [self.fan_speed_idle]
            self.fan_speed_min = [self.fan_speed_min]
            self.unit_scale = [self.unit_scale]
            self.fan_speed_max = [self.fan_speed_max]
            self.revolution_per_minute = [self.revolution_per_minute]
            self.max_deviation = [self.max_deviation ]

    async def initialize_device(self):
        """
        Initialize the fan unit.
        """
        await super().initialize_device()
        # Additional initialization logic can be added here if needed.

    def scale_output_fan_speed(self, x, in_min, in_max, out_min, out_max):
        try:
            return_val = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        except:
            return_val = 0
        return return_val

    async def set_fan_speed(self, manual_fan_speed=None):
        self.used_fan_speed.clear()
        if manual_fan_speed is None:
            for i in range(len(self.unit_channel)):
                await self.endpoint.set_speed(self.unit_channel[i], self.fan_speed_min[i])
                self.used_fan_speed.append(self.fan_speed_min[i])
        else:
            for i in range(len(self.unit_channel)):
                await self.endpoint.set_speed(self.unit_channel[i], manual_fan_speed)
                self.used_fan_speed.append(manual_fan_speed)

    async def get_fan_speed(self):
        fan_speed = list()
        for i in range(len(self.unit_channel)):
            if GlobalVar.get_stop_gc():
                return
            # try several common method name variants on the endpoint
            method = None
            for name in ["GetSpeed", "get_speed", "Get_Speed", "GetFanSpeed", "getFanSpeed", "get_speed_value"]:
                method = getattr(self.endpoint, name, None)
                if callable(method):
                    break
            if method is None:
                raise AttributeError(f"{type(self.endpoint).__name__!r} has no GetSpeed method; tried {['GetSpeed','get_speed','Get_Speed','GetFanSpeed','getFanSpeed','get_speed_value']}")

            # call the method and accept various return formats
            result = await method(self.unit_channel[i])
            # normalize different possible return types to a single speed value
            speed_val = None
            if isinstance(result, int):
                speed_val = result
            elif isinstance(result, float):
                speed_val = int(result)
            elif isinstance(result, (list, tuple)) and len(result) > 0:
                speed_val = result[0]
            elif isinstance(result, dict):
                for key in ("value", "speed", "Speed", "val"):
                    if key in result:
                        speed_val = result[key]
                        break
            else:
                # last resort: try to convert to int (handles numeric strings)
                try:
                    speed_val = int(result)
                except Exception:
                    # keep raw result if conversion fails
                    speed_val = result

            fan_speed.append(int(speed_val) * float(self.unit_scale[i]))
        return fan_speed

    async def compare_fan_speed(self):
        current_fan_speed = await self.get_fan_speed()
        self.fan_speed_list = []
        return_val = True

        if self.revolution_per_minute[0] > 0:
            for i in range(len(self.unit_channel)):
                scaled_fan_speed = self.scale_output_fan_speed(x=current_fan_speed[i],
                                                               in_min=0,
                                                               in_max=self.revolution_per_minute[i],
                                                               out_min=0,
                                                               out_max=100)
                self.fan_speed_list.append(round(scaled_fan_speed, 1))
                current_deviation = abs(scaled_fan_speed - self.used_fan_speed[i])

                if (current_deviation > self.max_deviation[i]):
                    return_val = False

        return return_val

    async def enable(self):
        await self.enable()

    async def disable(self):
        await self.disable()
