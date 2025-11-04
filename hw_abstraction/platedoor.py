from devicepilot.config_enum import mover_enum
from devicepilot.hw_abstraction.mover_ctrl import Mover
from config_enum import platedoor_enum


class PlateDoor(Mover):
    def __init__(self, hal_enum):
        '''
        hal_enum : need for Name and simulation
        '''
        super().__init__( hal_enum)


    async def open(self):
        await self.move_to_named_position(platedoor_enum.Positions.OpenPos)

    async def close(self):
        await self.move_to_named_position(platedoor_enum.Positions.ClosedPos)