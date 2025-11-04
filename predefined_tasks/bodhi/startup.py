from devicepilot.py_pli.pylib import GlobalVar
from devicepilot.pylog.pylogger import PyLogger
from predefined_tasks.common.helper import send_to_gc
from devicepilot.export.pli import hal

plateDoor = hal.plate_door
#scanTable = hal.scan_table
LightSwitchEmission = hal.light_switch_emission
LightSwitchExcitation = hal.light_switch_excitation
MonochromatorEmission = hal.monochromator_emission
MonochromatorExcitation = hal.monochromator_excitation
FilterWheelPMT = hal.filter_wheel_pmt
FilterWheelFlashLamp = hal.filter_wheel_flashlamp
UpperMeasureHead = hal.upper_measure_head

#MeasurementUnit = hal.measurement_unit

virtual_units = [
    #plateDoor,
    #scanTable,
    LightSwitchEmission,
    LightSwitchExcitation,
    MonochromatorEmission,
    MonochromatorExcitation,
    FilterWheelPMT,
    FilterWheelFlashLamp,
    UpperMeasureHead
]


async def home_vu(vu):
    #try:
    
    await send_to_gc(f'Homing {vu.name:<30}')
    step_error = await vu.home()
    if isinstance(step_error, (int, float)):
        step_errors = [step_error]
    elif isinstance(step_error, (tuple, list)):
        step_errors = list(step_error)
    await send_to_gc(f'Homing {vu.name:<30}{f"StepError:":<10}{step_error}')

    # except Exception as e:
    #     await send_to_gc(f'Error homing {vu.name}: {e}', log=True, error=True)
    #     PyLogger.logger.error(f'Error homing {vu.name}: {e}')
    #     return False
    
async def test():
    print('test called ======================================')
    #await scanTable.move(0,0)
    print('test done ======================================')

async def initialize_all_units():
    print('initialize_all_units called ======================================')
    #GlobalVar.set_stop_gc(False)
    #await send_to_gc(f'Startup Firmware...')
    #await startupFirmware()
    
    for vu in virtual_units:
        if vu:
            if GlobalVar.get_stop_gc():
                await send_to_gc(f'Script stopped by user')
                return
            print(f'Initialize {vu.name}... ======================================')
            await send_to_gc(f'Initialize {vu.name}...')
            await vu.initialize_device()

    print('Initialize MeasurementUnit... ======================================')
    
    #await MeasurementUnit.InitializeDevice()
    print('Initialize MeasurementUnit done ======================================')

    #await MeasurementUnit.Set_PMT_HV_FI(True)
    print('Set PMT HV FI done ======================================')
    #await send_gc_event("RefreshProgressBar", prog_value=0)
    await send_to_gc(f'Initialize all units done')


async def home_all_movers():
    print('home_all_movers called ======================================')
    for vu in virtual_units:
        if vu:
            if GlobalVar.get_stop_gc():
                await send_to_gc('Script stopped by user')
                return
            print(f'Homing {vu.name:<30} ======================================')
            
            await send_to_gc(f'Homing {vu.name:<30}')

            step_error = await vu.home()

            if isinstance(step_error, (int, float)):
                step_errors = [step_error]
            elif isinstance(step_error, (tuple, list)):
                step_errors = list(step_error)

            if hasattr(vu, 'step_error'):
                await send_to_gc(f'Homing {vu.name:<30}{f"StepError:":<10}{step_error}, error limit: ± {vu.last_homing_error}')
                
                if any(abs(err) > vu.step_error for err in step_errors):
                    await send_to_gc(f'Check {vu.name}, error limit is ± {vu.last_homing_error}')
            else:
                await send_to_gc(f'Homing {vu.name:<30}{f"StepError:":<10}{step_error}')
