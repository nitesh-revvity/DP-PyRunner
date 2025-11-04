from devicepilot.hw_abstraction.hardware_controller_base import HardwareCtrlBase
from devicepilot.pylog.pylogger import PyLogger
import asyncio


class MeasurementUnit(HardwareCtrlBase):
    """Minimal hardware-abstraction shim for a Measurement Unit.
    Inherits from HardwareCtrlBase to integrate with the HAL endpoint_factory/creation flow.
    This implementation is intentionally defensive: it will not raise if the URPC endpoint
    or simulation endpoint is missing or of an unexpected type.
    """

    def __init__(self, hal_vu_enum=None):
        # call base initializer which sets up can_id, config mapping and endpoint helper methods
        super().__init__(hal_vu_enum)
        self.hal_vu_enum = hal_vu_enum
        self.endpoint = None
        # try to create an endpoint using common measurement endpoint classes if endpoint_factory is present
        try:
            endpoint_class = None
            endpoint_class_sim = None
            # try common module/class names (wrapped in try/except to avoid import errors)
            try:
                from devicepilot.urpc.measurementfunctions import MeasurementFunctions as EndpointClass
                endpoint_class = EndpointClass
            except Exception:
                try:
                    from devicepilot.urpc.measurementsimfunctions import MeasurementFunctions as EndpointClass
                    endpoint_class = EndpointClass
                except Exception:
                    endpoint_class = None

            try:
                from devicepilot.urpc_sim.measurementfunctions_sim import MeasurementFunctionsSim as EndpointClassSim
                endpoint_class_sim = EndpointClassSim
            except Exception:
                try:
                    from devicepilot.urpc_sim.measurementsimfunctions_sim import MeasurementSimFunctions as EndpointClassSim
                    endpoint_class_sim = EndpointClassSim
                except Exception:
                    endpoint_class_sim = None

            if hasattr(self, 'endpoint_factory') and (endpoint_class is not None or endpoint_class_sim is not None):
                try:
                    # endpoint_factory implementations usually accept (endpoint_class, endpoint_class_sim)
                    self.endpoint = self.endpoint_factory(endpoint_class, endpoint_class_sim)
                except Exception as e:
                    PyLogger.logger.debug(f"MeasurementUnit: endpoint_factory call failed: {e}")
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.__init__ endpoint setup skipped: {e}")

    def initialize_device(self):
        """Synchronous initialization hook (kept for API compatibility)."""
        PyLogger.logger.debug(f"MeasurementUnit.initialize_device() for {getattr(self.hal_vu_enum, 'name', None)}")

    async def InitializeDevice(self):
        """Async initialization used by other virtual units; safe no-op if endpoint missing."""
        PyLogger.logger.debug(f"MeasurementUnit.InitializeDevice() for {getattr(self.hal_vu_enum, 'name', None)}")
        # try best-effort initialization using endpoint if available
        try:
            if hasattr(self, 'endpoint') and self.endpoint is not None and hasattr(self.endpoint, 'SetParameter'):
                # example: enable events on real endpoint if supported
                try:
                    await self.endpoint.SetParameter('InterlockEventEnable', 1)
                except Exception:
                    # ignore if parameter not supported or signature differs
                    pass
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.InitializeDevice: endpoint init skipped: {e}")

    def subscribe_for_interlock_events(self):
        try:
            if self.endpoint and hasattr(self.endpoint, 'subscribeSendInterlockEvent'):
                self.endpoint.subscribeSendInterlockEvent(self.on_interlock_event)
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.subscribe_for_interlock_events failed: {e}")

    def unsubscribe_for_interlock_events(self):
        try:
            if self.endpoint and hasattr(self.endpoint, 'unsubscribeSendInterlockEvent'):
                self.endpoint.unsubscribeSendInterlockEvent(self.on_interlock_event)
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.unsubscribe_for_interlock_events failed: {e}")

    def subscribe_for_error_events(self):
        try:
            if self.endpoint and hasattr(self.endpoint, 'subscribeSendErrorEvent'):
                self.endpoint.subscribeSendErrorEvent(self.on_error_event)
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.subscribe_for_error_events failed: {e}")

    def unsubscribe_for_error_events(self):
        try:
            if self.endpoint and hasattr(self.endpoint, 'unsubscribeSendErrorEvent'):
                self.endpoint.unsubscribeSendErrorEvent(self.on_error_event)
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.unsubscribe_for_error_events failed: {e}")

    async def get_interlock_status(self):
        """Return a simple interlock status integer. If endpoint not available return 0 (safe).
        The returned value is intentionally minimal; callers can adapt if they expect a richer type.
        """
        try:
            if not self.endpoint:
                return 0
            # try common call patterns
            if hasattr(self.endpoint, 'GetParameter'):
                try:
                    val = await self.endpoint.GetParameter('InterlockStatus')
                    # normalize results like lists/tuples
                    if isinstance(val, (list, tuple)) and len(val) > 0:
                        return int(val[0])
                    return int(val)
                except Exception:
                    pass
            if hasattr(self.endpoint, 'GetInterlockStatus'):
                try:
                    val = await self.endpoint.GetInterlockStatus()
                    if isinstance(val, (list, tuple)) and len(val) > 0:
                        return int(val[0])
                    return int(val)
                except Exception:
                    pass
        except Exception as e:
            PyLogger.logger.debug(f"MeasurementUnit.get_interlock_status failed: {e}")
        return 0

    # passthrough helpers for external callers/tests
    async def SetParameter(self, *args, **kwargs):
        if not self.endpoint or not hasattr(self.endpoint, 'SetParameter'):
            PyLogger.logger.debug("MeasurementUnit.SetParameter skipped: endpoint missing or not supporting SetParameter")
            return None
        return await self.endpoint.SetParameter(*args, **kwargs)

    async def GetParameter(self, *args, **kwargs):
        if not self.endpoint or not hasattr(self.endpoint, 'GetParameter'):
            PyLogger.logger.debug("MeasurementUnit.GetParameter skipped: endpoint missing or not supporting GetParameter")
            return None
        return await self.endpoint.GetParameter(*args, **kwargs)

    # default event handlers (can be overridden by wiring code)
    async def on_interlock_event(self, *args, **kwargs):
        PyLogger.logger.debug(f"MeasurementUnit.on_interlock_event called: {args} {kwargs}")

    async def on_error_event(self, *args, **kwargs):
        PyLogger.logger.debug(f"MeasurementUnit.on_error_event called: {args} {kwargs}")
