# Real Time Data Pipeline

rtdp is a real time data pipeline application that uses Apache Kafka, the Faust python library from Robinhood, and Elasticsearch.

The publisher polls the coindesk api and publishes a message to a Kafka topic.

The consumer subscribes to the kafka topic, pulls messages as they come in and then adds the data to elasticsearch document store.

# Installation and Usage

1. Pull images from Docker hub.
	`docker pull  wurstmeister/zookeeper`
	`docker pull wurstmeister/kafka`
	`docker pull elasticsearch:7.8.0`
2. Build rtdp docker image.
	`make build`
3. Bring up the containers
	`docker-compose up`
