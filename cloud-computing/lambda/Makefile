all: up

up:
	docker-compose -f zoo/docker-compose.yml up -d && docker-compose -f kafka/docker-compose.yml up -d

reup:
	make stop && docker-compose -f zoo/docker-compose.yml rm && docker-compose -f kafka/docker-compose.yml rm && make up

stop:
	docker-compose -f zoo/docker-compose.yml stop && docker-compose -f kafka/docker-compose.yml stop

list-topic:
	kafka/bin/kafka-topics.sh --list --zookeeper localhost:2181

producer-1:
	kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

producer-2:
	kafka/bin/kafka-console-producer.sh --broker-list localhost:9093 --topic test

consumer:
	kafka/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning
