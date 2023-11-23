from KafkaMessageConsumer import KafkaMessageConsumer
import TeamsMonitoring as tm 

import os
from typing import AnyStr
import sqlite3
import configparser
import contextlib
import logging

from prometheus_client import start_http_server, Counter

# Set logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s ::%(levelname)s::%(name)s --> %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Initialize Prometheus metrics
message_counter = Counter('messages_processed', 'Number of messages processed')

# The Kafka broker to connect to.
# By default this is set to kafka:9092. If you are running this script from
# outside of the docker container, then please set the KAFKA_BROKER environment
# variable to "localhost:9094".

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Get configuration values
KAFKA_BROKER = config.get("AppConfig", "KAFKA_BROKER")
KAFKA_TOPIC = config.get("AppConfig", "KAFKA_TOPIC")
CONSUMER_GROUP_ID = config.get("AppConfig", "CONSUMER_GROUP_ID")
SQLITE_DB_PATH = config.get("AppConfig", "SQLITE_DB_PATH")
SQLITE_TIMEOUT_SECONDS = config.getint("AppConfig", "SQLITE_TIMEOUT_SECONDS")
TEAMS = config.get("AppConfig", "TEAMS").split(',')
SENDER_EMAIL = config.get("AppConfig", "SENDER_EMAIL")

@contextlib.contextmanager
def connect_to_database(db_path: str, timeout: int):
    """Context manager for connecting to the SQLite database."""
    connection = sqlite3.connect(db_path, timeout=timeout)
    try:
        yield connection
    finally:
        connection.close()

def update_aggregated_data(msg: dict, db_path: str, timeout: int):

    with connect_to_database(db_path, timeout) as conn:
        cursor = conn.cursor()

        # Get the (potentially) already existing value for this category
        result = cursor.execute("SELECT count FROM aggregated WHERE food = ?", (msg['food'],))
        rows = result.fetchall()
        count = 0

        # Increment by one and update the row
        if len(rows) > 0:
            count = rows[0][0] + 1

        result = cursor.execute(
            "INSERT OR REPLACE INTO aggregated (food, count) VALUES (?, ?)",
            (msg['food'], count),
        )
        message_counter.inc()

        conn.commit()

def message_handler(topic: AnyStr, msg: dict):
    """Called for every message that is consumed from the Kafka topic. This is a sample
    implementation of what needs to be turned into a proper data pipeline as a goal of
    this assignment.

    Args:
        topic (AnyStr): the topic the message is consumed from
        msg (dict): the message as published on the Kafka topic
    """

    logger.info(f"Received a message on topic {topic}: {msg}")

    if "food" in msg:
        update_aggregated_data(msg, SQLITE_DB_PATH, SQLITE_TIMEOUT_SECONDS)
    else:
        
        error_message = f"message is malformed. Not processing.: {str(msg)}"
        tm.send_email(subject = 'Failure Notification - kafka', err_message=error_message, teams=TEAMS, sender_email=SENDER_EMAIL)


if __name__ == "__main__":
    # Connect to the Kafka bus and start consuming messages.
    consumer = KafkaMessageConsumer(KAFKA_TOPIC, KAFKA_BROKER, CONSUMER_GROUP_ID)
    start_http_server(8000) 
    consumer.start_blocking(message_handler)
