from devicepilot.py_pli.pylib import GlobalVar
from devicepilot.pylog.pylogger import PyLogger
from predefined_tasks.common.helper import send_to_gc
from devicepilot.export.pli import hal



plate_door_sensor = hal.mc6  # Assuming the Plate Door Sensor is connected to the MC6 node

async def get_plate_door_sensor_state():
    print('get_plate_door_sensor_state called ======================================')
    if plate_door_sensor:
        if GlobalVar.get_stop_gc():
            return
        sensor_state = await plate_door_sensor.get_sensor_input()
        await send_to_gc(f'Plate Door Sensor State: {sensor_state}')
    else:
        await send_to_gc('Plate Door Sensor not configured.', log=True, error=True)
        PyLogger.logger.error('Plate Door Sensor not configured.')