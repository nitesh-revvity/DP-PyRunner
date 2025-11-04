import asyncio
import numpy as np
from devicepilot.common import helper

from devicepilot.hw_abstraction.dual_mover_ctrl import DualMover
from config_enum import scan_table_enum
from config_enum import upper_measure_head_enum
from devicepilot.pylog.pylogger import PyLogger

# import after installation to ensure module availability
from jrpc_data.platedimensions import PlateDimensions # noqa: E402 


def plate_dimensions_to_mm(plate_dimensions: PlateDimensions):
    plate_dimensions.WellDiameterTop /= 100
    plate_dimensions.WellDiameterBottom /= 100
    plate_dimensions.CornerWell1X /= 100
    plate_dimensions.CornerWell1Y /= 100
    plate_dimensions.CornerWell2X /= 100
    plate_dimensions.CornerWell2Y /= 100
    plate_dimensions.CornerWell3X /= 100
    plate_dimensions.CornerWell3Y /= 100
    plate_dimensions.CornerWell4X /= 100
    plate_dimensions.CornerWell4Y /= 100
    plate_dimensions.Height /= 100
    plate_dimensions.WellDepth /= 100
    plate_dimensions.FlangeHeight /= 100

class ScanTable(DualMover):
    def __init__(self, hal_enum):
        '''
        hal_enum : need for Name and simulation
        '''
        super().__init__( hal_enum)
        self.__current_plate = None
        self.__currentProfile = None
        self.currentMeasPosX, self.currentMeasPosY = self.get_config(scan_table_enum.GC_Params.FI_Top_TopLeftCorner)


    def set_current_plate(self, plateDimensions):
        if plateDimensions.Height > 500:  # in 100th mm
            plate_dimensions_to_mm(plateDimensions)

        self.__currentPlate = plateDimensions

        dx12 = self.__currentPlate.CornerWell2X - self.__currentPlate.CornerWell1X
        dy12 = self.__currentPlate.CornerWell2Y - self.__currentPlate.CornerWell1Y

        self.v_a1_a12 = np.array([dx12, dy12])

        dx34 = self.__currentPlate.CornerWell4X - self.__currentPlate.CornerWell3X
        dy34 = self.__currentPlate.CornerWell4Y - self.__currentPlate.CornerWell3Y

        self.v_h1_h12 = np.array([dx34,dy34])

        dx13 = self.__currentPlate.CornerWell3X - self.__currentPlate.CornerWell1X
        dy13 = self.__currentPlate.CornerWell3Y - self.__currentPlate.CornerWell1Y

        self.v_a1_h1 = np.array([dx13, dy13])

        # if self.focusMover:
        #     self.focusMover.plateHeight = self.__currentPlate.Height
        # if self.usLumFocusMover:
        #     self.usLumFocusMover.plateHeight = self.__currentPlate.Height

    def get_current_profile(self):
        return self.__currentProfile
    
    
    async def move_to_well(self, col, row,  x_in_well_offset=0, y_in_well_offset=0, well2well=True, well_scan = False, tilt_correction=True):
        PyLogger.logger.info(f'scan_table_ctr.move_to_well({col}, {row}, {x_in_well_offset}, {y_in_well_offset} {self.__currentProfile})')

        if self.__currentPlate is None or self.currentMeasPosX is None or self.currentMeasPosY is None:
            raise Exception("No plate or meas pos set")

        if well2well and not self.single_mode_on and not self.__slowMode:
            await self.use_profile_single()

        if well_scan and not self.well_scan_mode_on and not self.__slowMode:
            await self.use_profile_wellscan()

        well_center_offset_x, well_center_offset_y = self.get_well_on_plate_offset(col=col, row=row)

        abs_pos_x, abs_pos_y = self.get_absolute_well_position(well_x_pos=well_center_offset_x, well_y_pos=well_center_offset_y,
                                                               x_in_well_offset=x_in_well_offset, y_in_well_offset=y_in_well_offset,
                                                               tilt_correction=tilt_correction)

        await self.move(abs_pos_x, abs_pos_y)

        settling_str = ""
        if self._settling_time_s != 0:
            await asyncio.sleep(self._settling_time_s)
            settling_str = f" (settling_time: {self._settling_time_s} s)"
        PyLogger.logger.debug(f'scan_table_ctr.move_to_well({col}, {row}, {x_in_well_offset}, {y_in_well_offset} - Ready' + settling_str)

