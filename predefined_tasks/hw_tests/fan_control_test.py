from devicepilot.py_pli.pylib import GlobalVar
from devicepilot.pylog.pylogger import PyLogger
from predefined_tasks.common.helper import send_to_gc
from devicepilot.export.pli import hal


air_ventilation_fan = hal.air_ventilation_fan
flashlamp_fan = hal.flashlamp_fan
groundplate_fan = hal.groundplate_fan


all_fans = [
    air_ventilation_fan,
    flashlamp_fan,
    groundplate_fan
]


async def get_fan_speed(fan: int = None):
    print('get_fan_speed called ======================================')
    if fan is None:
        for f in all_fans:
            if f:
                if GlobalVar.get_stop_gc():
                    return
                fan_speed = await f.get_fan_speed()
                await send_to_gc(f'Fan {f.name:<30} Speed: {fan_speed}')
    else:
        if 0 <= fan < len(all_fans):
            f = all_fans[fan]
            if f:
                if GlobalVar.get_stop_gc():
                    return
                fan_speed = await f.get_fan_speed()
                await send_to_gc(f'Fan {f.name:<30} Speed: {fan_speed}')
        else:
            await send_to_gc(f'Fan index {fan} is out of range.', log=True, error=True)
            PyLogger.logger.error(f'Fan index {fan} is out of range.')

async def set_fan_speed(fan: int = None, speed: int = None):
    print('set_fan_speed called ======================================')
    if fan is None:
        for f in all_fans:
            if f:
                if GlobalVar.get_stop_gc():
                    return
                await f.set_fan_speed(speed)
                await send_to_gc(f'Set Fan {f.name:<30} Speed to: {speed}')
    else:
        if 0 <= fan < len(all_fans):
            f = all_fans[fan]
            if f:
                if GlobalVar.get_stop_gc():
                    return
                await f.set_fan_speed(speed)
                await send_to_gc(f'Set Fan {f.name:<30} Speed to: {speed}')
        else:
            await send_to_gc(f'Fan index {fan} is out of range.', log=True, error=True)
            PyLogger.logger.error(f'Fan index {fan} is out of range.')  
    

