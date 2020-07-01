"""Faust consumer agent for Events Stream."""
import logging
import json

from faust import EventT

from rtdp.es.price_document import Tick, SEARCH_ES_ALIAS

LOGGER = logging.getLogger(__name__)


def consume(event: EventT) -> None:
    """Run the agent consumer."""
    try:
        data = json.loads(event.value.decode("utf-8"))
        LOGGER.debug("agent consumer data: %s", data)
    except Exception:
        LOGGER.exception("agent consumer exception.")
    tick = Tick(data)
    tick.save(using=SEARCH_ES_ALIAS)
    LOGGER.debug("Agent consumer saved elasticsearch document.")
