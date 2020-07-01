"""Faust application for consuming real time data."""

import faust

from rtdp.consumer.agents import agent
from rtdp import config

from rtdp.es import es, price_document

# Attempt to create an index mapping before doing any processing.
es.create_doc_mapping(price_document.Tick, price_document.BACKING_ES_INDEX)
# Attempt to create an ALIAS for jobs, if it does not exist already.
es.create_index_alias(price_document.BACKING_ES_INDEX, price_document.SEARCH_ES_ALIAS)

APP = faust.App(
    config.DATA_CONSUMER_ID,
    broker=f"aiokafka://{config.KAFKA_BROKERS}",
    topic_replication_factor=config.KAFKA_TOPIC_REPLICATION_FACTOR,
    topic_partitions=config.KAFKA_TOPIC_PARTITIONS,
    web_enabled=False,
    stream_wait_empty=False,
    consumer_auto_offset_reset=config.CONSUMER_AUTO_OFFSET_RESET,
    broker_max_poll_records=config.CONSUMER_POLL_MAX_MESSAGES,
    key_serializer="raw",
    value_serializer="raw"
    )

FAUST_TOPIC = APP.topic(config.KAFKA_TOPIC, partitions=config.KAFKA_TOPIC_PARTITIONS)

if config.CONSUMERS_AGENT_ENABLED:
    @APP.agent(FAUST_TOPIC, concurrency=config.CONSUMER_AGENT_CONCURRENCY)  # type: ignore
    async def agent_stream(events: faust.StreamT) -> None:
        """Start the faust consumer for the kafka topic."""
        async for event in events.events():
            agent.consume(event)
