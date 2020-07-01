"""Elasticsearch client wrappers."""
import logging
import os
import time

import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import Index
from elasticsearch_dsl.document import Document

from rtdp import config


ES_CONN_SLEEP_TIMER: int = 2
NUM_ES_CONN_RETRIES: int = 100

LOGGER = logging.getLogger(__name__)


def get_es_client(nowait: bool = False) -> Elasticsearch:
    """Get a new connection to Elasticsearch."""
    es_host = os.environ.get("ES_HOST", "http://elasticsearch:9200")

    if nowait:
        return create_es_client(es_host)

    LOGGER.info("Attempting to connect to ES...")

    for _ in range(1, NUM_ES_CONN_RETRIES):
        try:
            response = requests.get(f"{es_host}/_cluster/health?wait_for_status={config.ES_HEALTH_CHECK_COLOR}&timeout=30s") #pylint: disable=line-too-long
            response.raise_for_status()
        except Exception:
            LOGGER.exception("Could not connect to elasticsearch")
            time.sleep(ES_CONN_SLEEP_TIMER)
            continue

        try:
            es_client = create_es_client(es_host)
            cluster_client = es_client.cluster
            cluster_client.health(  # pylint: disable=unexpected-keyword-arg
                wait_for_status=config.ES_HEALTH_CHECK_COLOR)
            return es_client
        except Exception:
            time.sleep(ES_CONN_SLEEP_TIMER)

    raise ConnectionError


def create_es_client(es_host: str) -> Elasticsearch:
    """Create Elasticsearch client object. """
    es_verify_certs = os.environ.get("ES_VERIFY_CERTS", "false") == "true"
    es_use_ssl = os.environ.get("ES_USE_SSL", "false") == "true"
    es_client = Elasticsearch(
        [es_host],
        verify_certs=es_verify_certs,
        use_ssl=es_use_ssl,
        connection_class=RequestsHttpConnection,
    )
    return es_client


def create_index_alias(index: str, alias_name: str, force_create: bool = False) -> None:
    """Attempt to create an ES Alias for a given index if it does not exist already."""
    try:
        LOGGER.debug("Verifying Alias='%s' exists.", alias_name)
        alias_exists = Index(name=alias_name).exists_alias(
            using=get_es_client(), name=alias_name)
        if alias_exists and not force_create:
            LOGGER.debug("Alias='%s' exists already", alias_name)
            return
        LOGGER.debug("Alias did not exist. Creating Alias='%s' for index='%s'",
                     alias_name, index)
        Index(name=index).put_alias(using=get_es_client(), name=alias_name)
    except Exception:
        LOGGER.exception("Could not create Alias='%s'", alias_name)


def create_doc_mapping(doc: Document, index: str) -> None:
    """Attempt to create an ES mapping for a given document if it does not exist already."""
    try:
        LOGGER.debug("Preparing to create mapping")
        doc.init(using=get_es_client(), index=index)
        LOGGER.debug("Created mapping successfully")
    except Exception:
        LOGGER.exception("Could not create doc mapping")
