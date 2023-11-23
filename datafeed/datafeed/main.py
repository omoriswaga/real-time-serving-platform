from KafkaMessageProducer import KafkaMessageProducer
from Feed import Feed

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "message"


if __name__ == "__main__":
    producer = KafkaMessageProducer(KAFKA_TOPIC, KAFKA_BROKER)

    feed = Feed(producer)
    feed.start()
