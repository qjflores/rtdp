"""Config Variables for rtdp app"""

import os

KAFKA_BROKERS: str = os.environ.get("KAFKA_BROKERS", "kafka:9092")
KAFKA_TOPIC: str = os.environ.get("KAFKA_TOPIC", "dev-rtdp-topic")
KAFKA_TOPIC_PARTITIONS: int = os.environ.get("KAFKA_TOPIC_PARTITIONS", 1)

DATA_CONSUMER_ID: str = os.environ.get("DATA_CONSUMER_ID", "dev-rtdp-consumer-id")
KAFKA_TOPIC_REPLICATION_FACTOR: int = os.environ.get("KAFKA_TOPIC_REPLICATION_FACTOR", 1)
CONSUMER_AUTO_OFFSET_RESET: str = os.environ.get("CONSUMER_AUTO_OFFSET_RESET", "latest")
CONSUMER_POLL_MAX_MESSAGES: int = int(os.environ.get("CONSUMER_POLL_MAX_MESSAGES", 300))
CONSUMER_TABLE_STORE: str = f"{os.environ.get('DATA_CONSUMERS_TABLE_STORE', 'rocksdb')}://"


CONSUMER_AGENT_CONCURRENCY: int = int(os.environ.get("CONSUMER_AGENT_CONCURRENCY", 1))
CONSUMERS_AGENT_ENABLED: bool = os.environ.get("CONSUMERS_AGENT_ENABLED", True)

ES_HEALTH_CHECK_COLOR: str = os.environ.get("ES_HEALTH_CHECK_COLOR", "yellow")

TICKER_SYMBOL: str = os.environ.get("TICKER_SYMBOL", "XBT")
API_URL: str = os.environ.get("API_URL", f"https://api.coindesk.com/v1/bpi/currentprice/{TICKER_SYMBOL}.json") #pylint: disable=line-too-long
