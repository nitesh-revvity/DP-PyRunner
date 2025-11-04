from hw_abstraction.vu_filterwheel import VUFilterWheel

class FilterWheelFlashLamp(VUFilterWheel):
    def __init__(self, hal_vu_enum):
        super().__init__( hal_vu_enum)