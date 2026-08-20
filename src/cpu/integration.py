"""CPU Integration module for Project Phoenix (KAN-2).

Handles communication between the self-driving automation stack and
the vehicle's CPU/compute unit. Now integrates with the Firmware module
so commands are only executed when firmware is compatible and healthy.
"""

from src.firmware.firmware import Firmware

MINIMUM_SUPPORTED_FIRMWARE = "1.0.0"


def _version_tuple(version: str):
    return tuple(int(part) for part in version.split("."))


class CPUIntegration:
    def __init__(self, cpu_id: str, firmware: Firmware | None = None):
        self.cpu_id = cpu_id
        self.connected = False
        self.firmware = firmware or Firmware()
        self.command_log: list[str] = []

    def connect(self) -> bool:
        """Establish connection to the CPU, gated on firmware health and version.

        A real handshake would talk to hardware; here we simulate the same
        contract: connection only succeeds if firmware reports healthy and
        meets the minimum supported version.
        """
        if not self.firmware.is_healthy():
            self.connected = False
            return False

        if _version_tuple(self.firmware.check_version()) < _version_tuple(MINIMUM_SUPPORTED_FIRMWARE):
            self.connected = False
            return False

        self.connected = True
        return self.connected

    def send_command(self, command: str) -> str:
        if not self.connected:
            raise ConnectionError("CPU not connected. Call connect() first.")

        if not self.firmware.is_healthy():
            self.connected = False
            raise RuntimeError("Firmware became unhealthy; connection dropped.")

        self.command_log.append(command)
        return f"Executed: {command} (firmware v{self.firmware.check_version()})"

    def resync_firmware(self) -> bool:
        """Re-check firmware state and reconnect if it recovered."""
        return self.connect()
