"""Elasticsearch Price Document class and related classes or functions."""

import os
import uuid
from typing import Any, Dict

from elasticsearch_dsl.document import Document
from elasticsearch_dsl import Float, Keyword, Date
from elasticsearch_dsl.connections import connections

#: Name of ES index the document will be inserted into.
BACKING_ES_INDEX: str = os.environ.get("BACKING_ES_INDEX", "rtdp")
#: Name of the Search Alias.
SEARCH_ES_ALIAS: str = os.environ.get("SEARCH_ES_ALIAS", "rtdp.prices")

connections.create_connection(
    SEARCH_ES_ALIAS,
    hosts=[os.environ.get("ES_HOST", "http://elasticsearch:9200")])


class Tick(Document):
    """Event as represented in Elasticsearch."""
    class Index:
        """Elasticsearch index. """
        name = BACKING_ES_INDEX

    id = Keyword()
    price = Float()
    ticker = Keyword()
    currency = Keyword()
    event_time = Date()

    def __init__(self, price_data: Dict[str, Any]) -> None:
        """Initialize the object."""
        super().__init__()
        self.meta.id = uuid.uuid4().hex
        self.price = price_data['bpi']['USD']['rate_float']
        self.ticker = 'XBT'
        self.currency = 'USD'
        self.event_time = price_data['time']['updatedISO']
