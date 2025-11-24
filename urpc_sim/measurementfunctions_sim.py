import asyncio

class MeasurementFunctionsSim:
    """Simulation endpoint class for Measurement Functions.
    """

    def __init__(self, canid):
        self.canid = canid

    @staticmethod
    def get_own_interface_version():
        interface_type = 6
        interface_major = 1
        interface_minor = 3
        return interface_type, interface_major, interface_minor
    
    async def get_interface_version(self, type: int, timeout=1):
        await asyncio.sleep(1)
        return type, 1, 3
    
    async def set_interface_version(self, type: int, major: int, minor: int):
        await asyncio.sleep(0)
        return
    
    async def reset(self):
        await asyncio.sleep(0)
        return
    
    async def get_status(self, timeout=1):
        await asyncio.sleep(0)
        return 0, 0
    
    async def set_parameter(self, number: int, value: int, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def get_parameter(self, number: int, timeout=1):
        await asyncio.sleep(0)
        return 0
    
    async def write_sequence(self, address: int, size: int, data: list, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def start_sequence(self, address: int, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def cancel_sequence(self, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def read_results(self, address: int, size: int, timeout=1):
        await asyncio.sleep(0)
        return [0]*size
    
    async def send_interlock_event(self, event_code: int, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def subscribe_send_interlock_event(self, event_code: int, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def unsubscribe_send_interlock_event(self, event_code: int, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def send_error_event(self, status: int):
        await asyncio.sleep(0)
        return
    
    def subscribe_send_error_event(self, callback, no_duplicates=True):
        pass

    def unsubscribe_send_error_event(self, callback):
        pass

    async def write(self, address: int, size: int, data: list, timeout=1):
        await asyncio.sleep(0)
        return
    
    async def read(self, address: int, size: int, timeout=1):
        await asyncio.sleep(0)
        return [0]*size
    
    
    

    

