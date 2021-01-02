import struct
import typing
import logging

from .enums import ColorNo
from .enums import IOType
from .enums import MessageType

logger = logging.getLogger(__name__)


class HubIOMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        if hasattr(cls, "io_type") and hasattr(cls, "registry"):
            cls.registry[cls.io_type] = cls
        return cls


class HubIO(metaclass=HubIOMetaclass):
    io_type: IOType
    registry: typing.Dict[IOType, typing.Any] = {}

    def __init__(self, hub, port):
        self.hub = hub
        self.port = port


class TrainMotor(HubIO):
    io_type = IOType.TrainMotor

    def set_speed(self, value):
        self.hub.send_message(
            struct.pack(
                "BBBBBBBB",
                MessageType.PortOutput,
                self.port,
                0x00,
                0x60,
                0x00,
                value,
                0x00,
                0x00,
            )
        )


class LMotor(HubIO):
    io_type = IOType.LMotor

    def set_speed(self, value):
        logger.info("Sending speed to LMotor on port %s: %s", self.port, value)

        self.hub.send_message(
            struct.pack(
                "BBBBBB",
                MessageType.PortOutput,
                self.port,
                0x00,
                0x07,
                0x1d,
                0x01,
            )
        )


class XLMotor(HubIO):
    io_type = IOType.XLMotor

    def set_speed(self, value):
        self.hub.send_message(
            struct.pack(
                "BBBBBB",
                MessageType.PortOutput,
                self.port,
                0x11,
                0x51,
                0x00,
                0xc1,
            )
        )


class LEDLight(HubIO):
    io_type = IOType.LEDLight

    def set_brightness(self, value):
        self.hub.send_message(
            struct.pack(
                "BBBBBBBB",
                MessageType.PortOutput,
                self.port,
                0x00,
                0x60,
                0x00,
                value,
                0x00,
                0x00,
            )
        )


class Voltage(HubIO):
    io_type = IOType.Voltage


class RGBLight(HubIO):
    io_type = IOType.RGBLight

    def set_rgb_color_no(self, color_no: ColorNo):
        self.hub.send_message(
            struct.pack(
                "BBBBBB", MessageType.PortOutput, self.port, 0x01, 0x51, 0x00, color_no
            )
        )


class Current(HubIO):
    io_type = IOType.Current
