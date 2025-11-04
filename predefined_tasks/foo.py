import devicepilot.export.pli as pli

from hw_abstraction.hal import HAL
from devicepilot.pylog.pylogger import PyLogger

def add(a, b):
  #  a  = config_enum.hal_enum.HAL.Mainboard

    c = b.get_config(a)
    return a

def c():
    return pli.hal

async def register_digital_input_event():
    import devicepilot.export.pli as pli

    hal: HAL = pli.hal
    await hal.mc6.configure_digital_input_event(0)


    async def digital_input_event_callback(number, event_type):
        PyLogger.logger.info(f"Digital Input Event: number = {number}, type = {event_type}")
        if event_type == 1:
            await hal.mc6.set_analog_output(2, 1.0)
        else:
            await hal.mc6.set_analog_output(2, 0.0)

    hal.mc6.subscribe_digital_input_event(digital_input_event_callback)
