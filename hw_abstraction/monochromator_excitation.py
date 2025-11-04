from hw_abstraction.vu_monochromator import VUMonochromator

class MonochromatorExcitation(VUMonochromator):
    def __init__(self, hal_vu_enum):
        super().__init__(hal_vu_enum)