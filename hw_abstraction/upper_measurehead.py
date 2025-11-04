from devicepilot.hw_abstraction.dual_mover_ctrl import DualMover
from config_enum import upper_measure_head_enum


class UpperMeasureHead(DualMover):
    def __init__(self, hal_vu_enum):
        super().__init__( hal_vu_enum)

    async def initialize_device(self):
        """
        Initialize the upper measure head device.
        """
        await super().initialize_device()
        # Additional initialization logic can be added here if needed.
        

    def _calc_measurement_height(self, focus_depth, meas_height):
        """
        Calculate the measurement height based on the focus depth.

        focus_depth: The depth at which the focus is set.
        meas_height: The height to which the mover should be moved.
        """
        if meas_height is None:
            meas_height = 0
        plate_bottom_z = self.get_config(upper_measure_head_enum.GC_Params.PlateBottomZ_mm)
        position = round(plate_bottom_z - focus_depth - meas_height, 2)
        return position

    async def goto_measurement_height_fi_top(self, meas_height):
        """
        Move the mover to the measurement height for FI_TOP.
        meas_height: The height to which the mover should be moved.
        This height is subtracted from the focus depth to calculate the final position.
        """
        focus_depth = self.get_config(upper_measure_head_enum.GC_Params.FocusDepth_FI_TOP_mm)
        position = self._calc_measurement_height(focus_depth, meas_height)
        await self.move(position, position)

    async def goto_measurement_height_abs(self, meas_height):
        """
        Move the mover to the measurement height for ABS.
        meas_height: The height to which the mover should be moved.
        This height is subtracted from the focus depth to calculate the final position.
        """
        focus_depth = self.get_config(upper_measure_head_enum.GC_Params.FocusDepth_ABS_mm)
        position = self._calc_measurement_height(focus_depth, meas_height)
        await self.move(position, position)

    async def goto_measurement_height_lum(self, meas_height):
        """
        Move the mover to the measurement height for LUM.
        
        meas_height: The height to which the mover should be moved.
        This height is subtracted from the focus depth to calculate the final position.
        """
        focus_depth = self.get_config(upper_measure_head_enum.GC_Params.FocusDepth_LUM_mm)
        position = self._calc_measurement_height(focus_depth, meas_height)
        await self.move(position, position)

    async def goto_measurement_height_transopt(self):
        """
        Move the mover to the transport position.
        """
        position = self.get_config(upper_measure_head_enum.Positions.Transport)
        await self.Move(position)

    async def goto_fi_top_position(self):
        """
        Move the mover to the FI top position.
        """
        position = self.get_config(upper_measure_head_enum.Positions.FI_Top)
        await self.move(position, position)

    async def goto_fi_bottom_position(self):
        """
        Move the mover to the FI bottom position.
        """
        position = self.get_config(upper_measure_head_enum.Positions.FI_Bottom)
        await self.move(position, position)

    async def goto_abs_position(self):
        """
        Move the mover to the ABS position.
        """
        position = self.get_config(upper_measure_head_enum.Positions.ABS)
        await self.move(position, position)

    async def goto_lum_position(self):
        """
        Move the mover to the LUM position.
        """
        position = self.get_config(upper_measure_head_enum.Positions.LUM)
        await self.move(position, position)

    async def get_max_position(self):
        """
        Get the maximum position of the mover.
        """
        return self.get_config(upper_measure_head_enum.Positions.Max)
    
    async def get_min_position(self):   
        """
        Get the minimum position of the mover.
        """
        return self.get_config(upper_measure_head_enum.Positions.Min)

    
    


    

    
    
