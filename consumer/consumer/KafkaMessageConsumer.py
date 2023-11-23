from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from typing import AnyStr, Callable
import os
import time
import json
import logging
import configparser

# Set logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s ::%(levelname)s::%(name)s --> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
KAFKA_CONNECT_WAIT_SECONDS = config.getint("AppConfig", "KAFKA_CONNECT_WAIT_SECONDS")


"""KafkaMessageConsumer is a Kafka implementation of the MessageConsumer class.
"""
class KafkaMessageConsumer:
    def __init__(self, topic: AnyStr, broker: AnyStr, group_id: AnyStr):
        """Constructs the KafkaMessageConsumer

        Args:
            topic (AnyStr): name of the Kafka topic to consume from
            broker (AnyStr): address of the broker
        """

        self._topic = topic
        self._consumer = self.connect_consumer(broker, group_id)

    def connect_consumer(self, broker: AnyStr, group_id: AnyStr) -> KafkaConsumer:
        """Connects to the Kafka broker. Will keep re-trying indefinitely
        until the connection is successful. 

        Args:
            broker (str): hostname and port of the Kafka broker

        Returns:
            KafkaConsumer: the connected consumer
        """

        logger.info(f'Connecting consumer to {broker}...')
        while True:
            try:
                consumer = KafkaConsumer(
                    bootstrap_servers=broker,
                    group_id=group_id,
                    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
                )

                consumer.subscribe(self._topic)
                break
            except NoBrokersAvailable:
                logger.info(f'Kafka broker {broker} appears not to be running yet, '
                      f'waiting {KAFKA_CONNECT_WAIT_SECONDS} seconds before reconnecting')

                # Add an intential delay such that we do not hammer the broker
                # when it is not fully initialized yet.
                time.sleep(KAFKA_CONNECT_WAIT_SECONDS)

        logger.info('.. consumer connected.')
        return consumer

    def start_blocking(self, handler: Callable):
        """Start consuming message from the Kafka topic. For each message the
        specified handler will be called, passing the message value as the first
        parameter.

        Args:
            handler (Callable): the handler to be called for each message
        """
        
        for msg in self._consumer:
            handler(msg.topic, msg.value)
