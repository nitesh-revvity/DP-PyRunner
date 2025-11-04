from hw_abstraction.vu_light_switch import VULightSwitch

class LightSwitchExcitation(VULightSwitch):
    def __init__(self, hal_vu_enum):
        super().__init__( hal_vu_enum)