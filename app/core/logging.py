import logging
from pythonjsonlogger import jsonlogger
from app.core.config import settings

def configure_logging():
    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL)
    # avoid duplicate handlers in reload dev
    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        handler = logging.StreamHandler()
        fmt = '%(asctime)s %(levelname)s %(name)s %(message)s'
        formatter = jsonlogger.JsonFormatter(fmt)
        handler.setFormatter(formatter)
        root.addHandler(handler)

def get_logger(name: str = None):
    return logging.getLogger(name)
