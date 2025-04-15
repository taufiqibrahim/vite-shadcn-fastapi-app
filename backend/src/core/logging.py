import logging
from src.core.config import settings

log_level_str = settings.LOG_LEVEL.upper()
log_level = getattr(logging, log_level_str, logging.WARNING)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)
