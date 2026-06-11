import logging
from colorama import Fore, Style, init

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    """A logging formatter that adds ANSI colors based on log level."""
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        record.msg = f"{color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

    def __init__(self):
        super().__init__("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")


class JsonFormatter(logging.Formatter):
    """A formatter that outputs log records as JSON lines."""
    def __init__(self, ensure_ascii: bool = False):
        self.ensure_ascii = ensure_ascii
        super().__init__()

    def format(self, record):
        import json
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=self.ensure_ascii)
