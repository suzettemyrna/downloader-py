import sys
import os

class Reporter:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.exit_required = False

    def _write_to_file(self, message):
        if self.log_file:
            if os.path.isfile(self.log_file):
                with open(self.log_file, "a") as f:
                    f.write(message + "\n")

    def info(self, message):
        print(f"INFO: {message}")
        self._write_to_file(f"INFO: {message}")

    def error(self, message):
        print(f"ERROR: {message}", file=sys.stderr)
        self._write_to_file(f"ERROR: {message}")

    def fatal(self, message):
        print(f"FATAL: {message}", file=sys.stderr)
        self._write_to_file(f"FATAL: {message}")
        self.exit_required = True