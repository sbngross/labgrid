# FIXME
"""All CAN-related drivers"""
import attr

from ..factory import target_factory
from ..resource.remote import NetworkCanBus
from ..step import step
from .common import Driver
from ..util.agentwrapper import AgentWrapper


@target_factory.reg_driver
@attr.s(eq=False)
class CanBusDriver(Driver):

    bindings = {
        "bus": {"CanBus", "NetworkCanBus"},
    }

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.wrapper = None

    def on_activate(self):
        if isinstance(self.bus, NetworkCanBus):
            host = self.bus.host
        else:
            host = None
        self.wrapper = AgentWrapper(host)
        self.proxy = self.wrapper.load('canbus')

    def on_deactivate(self):
        self.wrapper.close()
        self.wrapper = None
        self.proxy = None

    @Driver.check_active
    @step(args=['arbitration', 'data'])
    def send(self, arbitration, data):
        self.proxy.send(self.bus.dev, arbitration, data)
