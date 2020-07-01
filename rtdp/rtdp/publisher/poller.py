"""
    Poller polls a given public api and uses the publisher
    to Publish to a kafka topic.
"""

import logging
import time

import requests

from rtdp.config import KAFKA_TOPIC
from rtdp.publisher.publisher import Publisher

LOGGER = logging.getLogger(__name__)


class Poller():
    """Poller class object for polling an api and sending kafka message."""
    def __init__(self, api):
        """Initialize the Poller with an api url and a Publisher"""
        self.api = api
        self.publisher = Publisher()

    def poll(self):
        """Poll the api and publish a the content to Kafka."""
        while True:
            response = requests.get(self.api)
            content = response.content
            LOGGER.debug("api content %s", content)
            self.publisher.publish(KAFKA_TOPIC, content)
            time.sleep(10)
