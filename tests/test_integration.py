"""Basic tests demonstrating CPU-firmware integration (KAN-2 / KAN-3)."""

from src.cpu.integration import CPUIntegration
from src.firmware.firmware import Firmware


def test_connect_succeeds_with_healthy_current_firmware():
    cpu = CPUIntegration("cpu-01", firmware=Firmware(version="1.0.0", healthy=True))
    assert cpu.connect() is True


def test_connect_fails_with_unhealthy_firmware():
    cpu = CPUIntegration("cpu-01", firmware=Firmware(version="1.0.0", healthy=False))
    assert cpu.connect() is False


def test_connect_fails_with_outdated_firmware():
    cpu = CPUIntegration("cpu-01", firmware=Firmware(version="0.5.0", healthy=True))
    assert cpu.connect() is False


def test_send_command_requires_connection():
    cpu = CPUIntegration("cpu-01", firmware=Firmware())
    try:
        cpu.send_command("steer_left")
        assert False, "expected ConnectionError"
    except ConnectionError:
        pass


def test_send_command_after_connect_and_firmware_update():
    firmware = Firmware(version="1.0.0")
    cpu = CPUIntegration("cpu-01", firmware=firmware)
    cpu.connect()
    firmware.update("1.1.0")
    result = cpu.send_command("accelerate")
    assert "accelerate" in result
    assert "1.1.0" in result
