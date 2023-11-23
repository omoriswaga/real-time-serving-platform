from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from typing import AnyStr

from MessageProducer import MessageProducer

import json
import time

KAFKA_CONNECT_WAIT_SECONDS = 5

"""KafkaMessageProducer is a Kafka implementation of the MessageProducer class.
"""
class KafkaMessageProducer(MessageProducer):
    def __init__(self, topic: AnyStr, broker: AnyStr):
        """Constructs a MessageProducer

        Args:
            topic (AnyStr): the topic to send messages to
            broker (AnyStr): address of the broker
        """

        self._topic = topic
        self._producer = self.connect_producer(broker)

    def connect_producer(self, broker: AnyStr) -> KafkaProducer:
        """Connects the Kafka producer. Will re-try connecting indefinitely
        until the connection is successful.

        Args:
            broker (AnyStr): address of the broker

        Returns:
            KafkaProducer: the connected producer
        """        

        print(f'Connecting KafkaProducer to {broker}...')
        while True:
            try:
                producer = KafkaProducer(
                    bootstrap_servers=broker,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )
                break
            except NoBrokersAvailable:
                print(f'Kafka broker {broker} appears not to be running yet, ' \
                      f'waiting {KAFKA_CONNECT_WAIT_SECONDS} seconds before reconnecting')

                # Add an intential delay such that we do not hammer the broker
                # when it is not fully initialized yet.
                time.sleep(KAFKA_CONNECT_WAIT_SECONDS)

        print('.. producer connected.')
        return producer

    def send(self, msg: dict):
        """Send a new message to the topic

        Args:
            msg (dict): the message object
        """

        self._producer.send(self._topic, msg)
