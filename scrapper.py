import hashlib
import logging

logger: logging.Logger = logging.getLogger(__name__)


def get_page_hash(response) -> str:
    page_hash: str = hashlib.md5(response.content).hexdigest()
    logger.debug("Hash for %s: %s", response.url, page_hash)
    return page_hash
