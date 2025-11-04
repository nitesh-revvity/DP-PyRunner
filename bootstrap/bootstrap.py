from config_enum import hal_enum
from devicepilot.bootstrap.bootstraper import BootstrapBase


from hw_abstraction.hal import HAL


class Bootstrap(BootstrapBase):
    
    def setup(self):
        hal = HAL()
        self.register_hal(hal)