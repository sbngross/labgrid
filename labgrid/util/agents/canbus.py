# FIXME
"""
This module implements can stuff.

Takes a string property 'device' which refers the stuff.

"""
import can
import logging

BUS_TYPE = 'socketcan'
BUS_BITRATE = 1e6
BUS_TIMEOUT_SEC = 10


class CanBusDevice:

    def __init__(self, dev):
        self._logger = logging.getLogger("Device: ")

        self.bus = can.Bus(dev, BUS_TYPE, BUS_BITRATE)

    def __del__(self):
        self.bus.shutdown()

    def send(self, arbitration, data):
        msg = can.Message(arbitration, data)
        self._logger = logging.info(f"Msg: {repr(msg)}")
        self.bus.send(msg, BUS_TIMEOUT_SEC)


_buses = {}


def _get_bus_dev(dev: str):
    if dev not in _buses:
        _buses[dev] = CanBusDevice(dev=dev)
    return _buses[dev]


def handle_send(dev, arbitration, data):
    bus_dev = _get_bus_dev(dev)
    bus_dev.send(arbitration, data)


methods = {
    'send': handle_send,
}
