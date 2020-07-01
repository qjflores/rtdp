"""Publish messages to the Kafka topic."""

import logging

from kafka import KafkaProducer

from rtdp.config import KAFKA_BROKERS

LOGGER = logging.getLogger(__name__)


def on_send_success(record_metadata):
    """Callback function when a message is successfully sent to the topic."""
    LOGGER.debug("Publisher.on_send_success topic %s, partition %s, offset %s",
                 record_metadata.topic,
                 record_metadata.partition,
                 record_metadata.offset
                 )


def on_send_error(excp):
    """Callback function when an error occurs sending the message to the topic"""
    LOGGER.error("Publisher.on_send_error: %s", excp)


class Publisher(): #pylint: disable=too-few-public-methods
    """Publisher class to publish to messages to a kafka topic."""
    def __init__(self):
        """Init the Publish with a kakfa producer"""
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

    def publish(self, kafka_topic, msg):
        """Publish a message by sending the message to the topic."""
        self.producer.send(
            kafka_topic, msg).add_callback(
                on_send_success).add_errback(
                    on_send_error)
