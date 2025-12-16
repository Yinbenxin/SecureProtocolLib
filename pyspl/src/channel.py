import logging

try:
    from .spllib import CreateGrpclinks  # type: ignore[attr-defined]
except ModuleNotFoundError:
    try:
        from ..spllib import CreateGrpclinks  # type: ignore[attr-defined]
    except ModuleNotFoundError:
        from pyspl.spllib import CreateGrpclinks  # type: ignore[attr-defined]
