"""Firmware module for Project Phoenix (KAN-3).

Handles firmware version checks, health status, and updates used by the
CPU integration layer (KAN-2) to decide whether it's safe to operate.
"""


class Firmware:
    def __init__(self, version: str = "1.0.0", healthy: bool = True):
        self.version = version
        self.healthy = healthy
        self.update_history: list[str] = []

    def check_version(self) -> str:
        return self.version

    def is_healthy(self) -> bool:
        """Report firmware health. Placeholder for real diagnostics/heartbeat."""
        return self.healthy

    def update(self, new_version: str) -> bool:
        """Apply a firmware update.

        Marks firmware temporarily unhealthy during the (simulated) flash
        process, then healthy again once the new version is applied.
        """
        self.healthy = False
        self.update_history.append(f"{self.version} -> {new_version}")
        self.version = new_version
        self.healthy = True
        return True

    def mark_unhealthy(self) -> None:
        """Simulate a firmware fault, e.g. for testing CPU integration's response."""
        self.healthy = False
