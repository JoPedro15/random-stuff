import sys
from datetime import datetime
from typing import Final


class Logger:
    """
    Standardized ANSI-colored logger for automation pipelines.
    Provides clean, professional terminal output without icons or emojis.
    """

    HEADER: Final[str] = '\033[95m'
    BLUE: Final[str] = '\033[94m'
    GREEN: Final[str] = '\033[92m'
    WARNING: Final[str] = '\033[93m'
    FAIL: Final[str] = '\033[91m'
    ENDC: Final[str] = '\033[0m'
    BOLD: Final[str] = '\033[1m'

    @staticmethod
    def _get_timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def info(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self.BLUE}INFO:{self.ENDC} {message}")

    def success(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self.GREEN}SUCCESS:{self.ENDC} {message}")

    def warning(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self.WARNING}WARNING:{self.ENDC} {message}")

    def error(self, message: str) -> None:
        print(f"[{self._get_timestamp()}] {self.FAIL}ERROR:{self.ENDC} {message}", file=sys.stderr)

    def section(self, title: str) -> None:
        print(f"\n{self.BOLD}{self.HEADER}--- {title.upper()} ---{self.ENDC}")


logger: Logger = Logger()
