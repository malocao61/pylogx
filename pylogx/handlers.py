import logging
import os
import glob

class RotatingFileHandler(logging.Handler):
    """A handler that rotates log files when they exceed a size limit."""
    def __init__(self, filename, max_bytes=10_485_760, backup_count=5, encoding="utf-8"):
        super().__init__()
        self.filename = filename
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.encoding = encoding
        self._open_file()

    def _open_file(self):
        self.stream = open(self.filename, "a", encoding=self.encoding)

    def emit(self, record):
        try:
            msg = self.format(record) + "\n"
            self.stream.write(msg)
            self.stream.flush()
            if self.stream.tell() >= self.max_bytes:
                self._rotate()
        except Exception:
            self.handleError(record)

    def _rotate(self):
        self.stream.close()
        for i in range(self.backup_count - 1, 0, -1):
            src = f"{self.filename}.{i}"
            dst = f"{self.filename}.{i+1}"
            if os.path.exists(src):
                os.rename(src, dst)
        if os.path.exists(self.filename):
            os.rename(self.filename, f"{self.filename}.1")
        self._open_file()

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()


class TimedRotatingFileHandler(logging.Handler):
    """A handler that rotates log files at a specific time interval."""
    def __init__(self, filename, when="midnight", interval=1, backup_count=7, encoding="utf-8"):
        super().__init__()
        self.filename = filename
        self.when = when
        self.interval = interval
        self.backup_count = backup_count
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.rollover_at = self._compute_rollover()
        self._open_file()

    def _compute_rollover(self):
        import time
        now = time.time()
        if self.when == "midnight":
            t = time.localtime(now)
            next_midnight = time.mktime((t.tm_year, t.tm_mon, t.tm_mday + 1, 0, 0, 0, 0, 0, -1))
            return next_midnight
        else:
            return now + self.interval * 86400

    def _open_file(self):
        self.stream = open(self.filename, "a", encoding=self.encoding)

    def emit(self, record):
        import time
        try:
            if time.time() >= self.rollover_at:
                self._rotate()
            msg = self.format(record) + "\n"
            self.stream.write(msg)
            self.stream.flush()
        except Exception:
            self.handleError(record)

    def _rotate(self):
        import time
        self.stream.close()
        date = time.strftime(self.suffix)
        backup_name = f"{self.filename}.{date}"
        if os.path.exists(self.filename):
            os.rename(self.filename, backup_name)
        self._open_file()
        self.rollover_at = self._compute_rollover()
        self._cleanup()

    def _cleanup(self):
        backups = sorted(glob.glob(f"{self.filename}.*"))
        for old in backups[:-self.backup_count]:
            os.remove(old)

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()
