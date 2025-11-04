#from devicepilot.exports.pli import hal
from devicepilot.export.pli import hal



from devicepilot.py_pli.pylib import GlobalVar
#from devicepilot.py_pli.pylib import send_to_gc, send_gc_event
from devicepilot.pylog.pylogger import PyLogger
from predefined_tasks.common.helper import send_to_gc


async def monochromator_excitation_mover_go_to_zero_order():
    print('-------------------------------here is the hal-------------------------------------------------')
    print(hal.monochromator_emission.__dict__)
    print('--------------------------------end of hal------------------------------------------------')
    print("Monochromator excitation mover go to zero order")
    await hal.monochromator_emission.goto_zero_order()
    print('Monochromator excitation mover at zero order')
    print('--------------------------------------------------------------------------------')

async def monochromator_excitation_mover_go_to_wavelength(wavelength):
    print('--------------------------------------------------------------------------------')
    print(f"Monochromator excitation mover go to wavelength {wavelength}")
    await hal.monocromator_excitation.goto_wavelenght(wavelength)
    print(f'Monochromator excitation mover at wavelength {wavelength}')
    print('--------------------------------------------------------------------------------')


async def test_send_to_gc():
    """
    Test function to send a message to the gc output.
    """
    print("Starting test_send_to_gc function...")
    await send_to_gc("This is a test message", log=True)
    PyLogger.logger.debug("Test message sent to gc output.")
    print("Test message sent to gc output.")