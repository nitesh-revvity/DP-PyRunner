from devicepilot.pylog.pylogger import PyLogger
from config_enum  import monochromator_enum
from devicepilot.hw_abstraction.mover_ctrl import Mover
from devicepilot.urpc.moverfunctions import MoverFunctions
import numpy # type: ignore



class VUMonochromator(Mover):
    def __init__(self, hal_enum):
        super().__init__(hal_enum)
        self.endpoint: MoverFunctions = self.endpoint

    async def initialize_device(self):
        await super().initialize_device()

    async def goto_zero_order(self):
        await self.move_to_named_position(monochromator_enum.Positions.pos_zero_order)

    async def goto_wavelenght(self, waveLength):
        if waveLength is None or waveLength == 0:
            await self.goto_zero_order()
            return
        position = self.calc_wavelenght(waveLength)
        PyLogger.logger.debug(f'Monochromator move to wavelength = {waveLength} position = {position}')
        await self.move(position)

    async def get_wavelenght(self):
        return self.get_position()

    def calc_wavelenght(self, waveLenght_nm):

        min_waveLenght = self.get_config(monochromator_enum.Unit.Min_WaveLength)
        max_waveLenght = self.get_config(monochromator_enum.Unit.Max_WaveLength)

        pos_zero_order = self.get_config(monochromator_enum.Positions.pos_zero_order)
        pos_365nm = self.get_config(monochromator_enum.Positions.pos_at_365nm)
        pos_488nm = self.get_config(monochromator_enum.Positions.pos_at_488nm)
        pos_635nm = self.get_config(monochromator_enum.Positions.pos_at_635nm)
        pos_785nm = self.get_config(monochromator_enum.Positions.pos_at_785nm)


        if waveLenght_nm < min_waveLenght:
            waveLenght_nm = min_waveLenght

        if waveLenght_nm > max_waveLenght:
            waveLenght_nm = max_waveLenght

        #   https://scipy-lectures.org/intro/numpy/auto_examples/plot_polyfit.html
        x = numpy.array([0, 365, 488, 635, 785])
        y = numpy.array([pos_zero_order, pos_365nm, pos_488nm, pos_635nm, pos_785nm])
        z = numpy.poly1d(numpy.polyfit(x, y, 3))

        position = (z[3] * waveLenght_nm ** 3) + (z[2] * waveLenght_nm ** 2) + (z[1] * waveLenght_nm) + z[0]

        return position
    

    async def get_max_position(self):
        return self.get_config(monochromator_enum.Positions.Max)

    async def get_min_position(self):
        return self.get_config(monochromator_enum.Positions.Min)
