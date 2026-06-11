import logging
import sys
from typing import Optional

class Logger:
    """Main logger class with convenience methods."""
    
    def __init__(self, name: str, level: int = logging.INFO, use_colors: bool = True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        if use_colors and sys.stdout.isatty():
            formatter = ColorFormatter()
        else:
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, msg: str, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)
    
    def warn(self, msg: str, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg: str, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
    
    def debug(self, msg: str, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)
    
    def critical(self, msg: str, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)
    
    def add_handler(self, handler):
        self.logger.addHandler(handler)
    
    def set_level(self, level: int):
        self.logger.setLevel(level)


def get_logger(name: str, level: int = logging.INFO, use_colors: bool = True) -> Logger:
    """Factory to create a new logger instance."""
    return Logger(name, level, use_colors)
