from devicepilot.config_enum import mover_enum


class Positions(mover_enum.Positions):
    OpenPos = ''
    ClosedPos = ''


class Profile_Operation(mover_enum.Profile):
    pass


class Profile_Home(mover_enum.Profile):
    pass


class Profile_Test(mover_enum.Profile):
    pass


class TriggerPosition_Closed(mover_enum.TriggerPosition):
    pass
