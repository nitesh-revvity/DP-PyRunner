from devicepilot.hw_abstraction.hardware_controller_base import HardwareCtrlBase
from devicepilot.pylog.pylogger import PyLogger
from devicepilot.urpc.measurementfunctions import MeasurementFunctions
#from devicepilot.urpc_sim.measurementfunctions_sim import MeasurementFunctionsSim # Simulation endpoint class missiing in devicepilot?
from urpc_sim.measurementfunctions_sim import MeasurementFunctionsSim


class MeasurementUnit(HardwareCtrlBase):
    """Minimal hardware-abstraction shim for a Measurement Unit.
    Inherits from HardwareCtrlBase to integrate with the HAL endpoint_factory/creation flow.
    This implementation is intentionally defensive: it will not raise if the URPC endpoint
    or simulation endpoint is missing or of an unexpected type.
    """

    def __init__(self, hal_vu_enum=None):

        super().__init__(hal_vu_enum)
        self.hal_vu_enum = hal_vu_enum
        self.endpoint = None


