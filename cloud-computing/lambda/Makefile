all: up

up:
	docker-compose -f zoo/docker-compose.yml up -d && docker-compose -f kafka/docker-compose.yml up -d

stop:
	docker-compose -f zoo/docker-compose.yml stop && docker-compose -f kafka/docker-compose.yml stop

list-topic:
	kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181

producer:
	kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

consumer:
	kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning