import logging

try:
    from pyspl.src.spllib import CreateChannel  # type: ignore[attr-defined]
except ModuleNotFoundError:
    try:
        from pyspl.spllib import CreateChannel  # type: ignore[attr-defined]
    except ModuleNotFoundError:
        from .spllib import CreateChannel  # type: ignore[attr-defined]

from pyspl.src.psi import *

log_format_full_path = '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d:%(funcName)s] %(message)s'
log_format_short_path = '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s'

logging.basicConfig(
    level=logging.INFO,
    format=log_format_short_path,
)
