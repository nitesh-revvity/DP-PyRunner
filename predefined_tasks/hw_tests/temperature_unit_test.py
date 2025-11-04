from devicepilot.py_pli.pylib import GlobalVar
from devicepilot.pylog.pylogger import PyLogger
from predefined_tasks.common.helper import send_to_gc
from devicepilot.export.pli import hal



lower_heating = hal.lower_heating
upper_heating = hal.upper_heating

all_temperature_units = [
    lower_heating,
    upper_heating
]


async def set_target_temperature(unit: int = None, temperature: float = None):
    print('set_target_temperature called ======================================')
    if unit is None:
        for tu in all_temperature_units:
            if tu:
                if GlobalVar.get_stop_gc():
                    return
                await tu.set_target_temperature(temperature)
                await send_to_gc(f'Set Temperature Unit {tu.name:<30} Target Temperature to: {temperature}')
    else:
        if 0 <= unit < len(all_temperature_units):
            tu = all_temperature_units[unit]
            if tu:
                if GlobalVar.get_stop_gc():
                    return
                await tu.set_target_temperature(temperature)
                await send_to_gc(f'Set Temperature Unit {tu.name:<30} Target Temperature to: {temperature}')
        else:
            await send_to_gc(f'Temperature Unit index {unit} is out of range.', log=True, error=True)
            PyLogger.logger.error(f'Temperature Unit index {unit} is out of range.')

async def get_current_temperature(unit: int = None):
    print('get_current_temperature called ======================================')
    if unit is None:
        for tu in all_temperature_units:
            if tu:
                if GlobalVar.get_stop_gc():
                    return
                temp_values = await tu.get_temperature_values()
                await send_to_gc(f'Temperature Unit {tu.name:<30} Values: {temp_values}')
    else:
        if 0 <= unit < len(all_temperature_units):
            tu = all_temperature_units[unit]
            if tu:
                if GlobalVar.get_stop_gc():
                    return
                temp_values = await tu.get_temperature_values()
                await send_to_gc(f'Temperature Unit {tu.name:<30} Values: {temp_values}')
        else:
            await send_to_gc(f'Temperature Unit index {unit} is out of range.', log=True, error=True)
            PyLogger.logger.error(f'Temperature Unit index {unit} is out of range.')