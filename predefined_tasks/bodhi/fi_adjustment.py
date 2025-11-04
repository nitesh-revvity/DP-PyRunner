from devicepilot.py_pli.pylib import GlobalVar
from devicepilot.pylog.pylogger import PyLogger
from predefined_tasks.common.helper import send_to_gc
from devicepilot.export.pli import hal

import sys
import time

plateDoor = hal.plate_door
scanTable = hal.dual_mover_1
LightSwitchEmission = hal.light_switch_emission
LightSwitchExcitation = hal.light_switch_excitation
MonochromatorEmission = hal.monochromator_emission
MonochromatorExcitation = hal.monochromator_excitation
FilterWheelPMT = hal.filter_wheel_pmt
FilterWheelFlashLamp = hal.filter_wheel_flashlamp
UpperMeasureHead = hal.upper_measure_head


async def Calculate_Initial_Ref_Fi_Top(wavelength_range_min=230, wavelength_range_max=1000, flashes=500, sleep_sec=0.5, flash_lamp_low_power=False, with_init=1, iref0_avg_wavelength_range_min = 441, iref0_avg_wavelength_range_max = 460):
    #await send_script_details()

    report_file = report_path(sys._getframe().f_code.co_name)

    with open(report_file, 'w', newline='') as report:  # home/operator/logs/reports/
        #gc_write_header_to_report(report)

        #await check_and_execute_initialization_homing(with_init)

        try:
            start_time = time.time()
    
            if LightSwitchExcitation:
                await LightSwitchExcitation.GotoFiTopPosition()
            if FilterWheelFlashLamp:
                await FilterWheelFlashLamp.GotoMaxSignal()
            if str(flash_lamp_low_power).lower() == 'true':
                meas_time = get_meas_time(flashes=flashes, frequency=MeasurementUnit.get_config(measurement_unit_enum.GC_Params.FlashFrequency_lowPower))
                await Measurements.instance.fiMeas.hal.measurementUnit.EnableFlashLampPower(isLow=True)
                await send_to_gc(F"low flash_lamp_low_power: {flash_lamp_low_power}")
                flash_lamp_low_power = True
            else:
                meas_time = get_meas_time(flashes=flashes, frequency=MeasurementUnit.get_config(measurement_unit_enum.GC_Params.FlashFrequency_hiPower))
                await Measurements.instance.fiMeas.hal.measurementUnit.EnableFlashLampPower(isLow=False)
                await send_to_gc(F"high flash_lamp_low_power: {flash_lamp_low_power}")
                flash_lamp_low_power = False
            await send_to_gc(F"meas_time: {meas_time}")
            await Measurements.instance.fiMeas.test_init(top_meas=True, meas_time=meas_time, flash_lamp_low_power=flash_lamp_low_power)
            await Measurements.instance.fiMeas.hal.measurementUnit.Set_PMT_HV_FI(True)
            await send_to_gc('wavelength, initial_ref_signal', False, False, report)
            flash_lamp_power = "low" if flash_lamp_low_power == True else "high"
            final_table_dict = {
                "description": "Each key represents a wavelength in nanometers (nm), and each value represents the corresponding initial reference measurement.",
                "No of flashes per measurement": flashes,
                "Flashe lamp power": flash_lamp_power,
                "data":  {},
                "average": None
            }
            for wavelength in range(wavelength_range_min, wavelength_range_max + 1):
                if GlobalVar.get_stop_gc():
                    await send_to_gc(f'Script stopped by user')
                    return
                await FilterWheelFlashLamp.SetFilterByWavelenght(wavelength)
                await MonochromatorExcitationMover.GoToWaveLenght(wavelength)
    
                result = await Measurements.instance.fiMeas.execute()
                mean_refSignal = round(result.refSignal / flashes, 3)
                # final_table[i] = (wavelength, mean_refSignal)
                final_table_dict["data"][wavelength] = mean_refSignal
                await send_to_gc(f'{wavelength}, {mean_refSignal}', False, False, report)
                await asyncio.sleep(sleep_sec)

            Iref0FiTop_config_path = HAL.get_config(hal_enum.Application.Iref0PathFiTop)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            target_path = os.path.normpath(os.path.join(BASE_DIR, Iref0FiTop_config_path))

            await send_to_gc(f"target_path: {target_path}")
            existing_data = {}
            if os.path.exists(target_path):
                # Read the existing JSON data
                with open(target_path, 'r') as jsonfile:
                    try:
                        existing_data = json.load(jsonfile)["data"]
                        existing_data = {int(key): val for key, val in existing_data.items()}
                        existing_data.update(final_table_dict["data"])
                    except json.JSONDecodeError:
                        await send_to_gc(f"JSONDecodeError while extracting data from target file")
    
            if existing_data:
                final_table_dict["data"].update(existing_data)
                final_table_dict["data"] = {k: final_table_dict["data"][k] for k in sorted(final_table_dict["data"].keys())}

            iref0_avg = await calc_avg_iref(final_table_dict["data"], iref0_avg_wavelength_range_min, iref0_avg_wavelength_range_max)
            final_table_dict['average'] = iref0_avg
            await send_to_gc(f'iref0_avg: {iref0_avg}')

            with open(target_path, 'w') as jsonfile:
                json.dump(final_table_dict, jsonfile, indent=4)
    
        except:
            error = traceback.format_exc()
            await send_to_gc(str(error))
    
        finally:
            total_time = await cal_time(start_time)
            await send_to_gc(f"total_time: {total_time} sec")

