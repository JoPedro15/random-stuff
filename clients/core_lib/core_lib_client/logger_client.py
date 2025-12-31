import sys
from datetime import datetime
from typing import Final, Optional


class Logger:
    """
    Standardized ANSI-colored logger for automation pipelines.
    Provides clean, professional terminal output without icons or emojis.
    """

    _HEADER: Final[str] = '\033[95m'
    _BLUE: Final[str] = '\033[94m'
    _GREEN: Final[str] = '\033[92m'
    _WARNING: Final[str] = '\033[93m'
    _FAIL: Final[str] = '\033[91m'
    _ENDC: Final[str] = '\033[0m'
    _BOLD: Final[str] = '\033[1m'

    @staticmethod
    def _get_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def info(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] INFO: {message}")

    def success(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self._GREEN}SUCCESS:{self._ENDC} {message}")

    def warning(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self._WARNING}WARNING:{self._ENDC} {message}")

    def error(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self._FAIL}ERROR:{self._ENDC} {message}", file=sys.stderr)

    def section(self, title: str) -> None:
        print(f"\n{self._get_timestamp()}{self._BOLD}{self._HEADER}{title.upper()}{self._ENDC}")

    def print(self, message: str, color: Optional[str] = None) -> None:
        """Raw print replacement. No timestamp, no prefix. Optional color."""
        c = color if color else ""
        end = self._ENDC if color else ""
        print(f"{c}{message}{end}")


logger: Logger = Logger()
