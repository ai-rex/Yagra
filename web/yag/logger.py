import sys
from datetime import datetime

__all__ = ['err']

def err(name, message):
    log_format = '%s - %s - %s\n'
    sys.stderr.write(log_format % (datetime.now().isoformat(), name, message))

