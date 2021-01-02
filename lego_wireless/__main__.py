import atexit
import logging
import threading

from . import signals
from .manager import HubManager
from lego_wireless.hub_io import TrainMotor
from lego_wireless.hub_io import LMotor
from lego_wireless.hub_io import XLMotor

hubs_seen = set()


logger = logging.getLogger(__name__)


def hub_discovered(sender, hub):
    if hub not in hubs_seen:
        hubs_seen.add(hub)
        logger.info("Connecting Hub IO, %s", hub.mac_address)
        signals.hub_io_connected.connect(hub_io_connected, sender=hub)
        hub.connect()


def hub_io_connected(sender, hub_io):
    logger.info("IO connected: %s", hub_io.__class__.__name__)
    if isinstance(hub_io, TrainMotor):
        hub_io.set_speed(100)
    if isinstance(hub_io, LMotor):
        hub_io.set_no_rotation()
        hub_io.set_rotation_left()
        hub_io.set_no_rotation()
        hub_io.set_rotation_right()
    if isinstance(hub_io, XLMotor):
        hub_io.set_forward()


def main():
    hub_manager = HubManager("hci0")
    atexit.register(hub_manager.stop)

    signals.hub_discovered.connect(hub_discovered, sender=hub_manager)

    hub_manager_thread = threading.Thread(target=hub_manager.run)
    hub_manager_thread.start()
    hub_manager.start_discovery()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
