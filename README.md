# Coding Assignment - Data Events

Consider an imaginary system where we have a continuous inflow of events on a message bus. Each event message indicate the occurence of a food item in a certain category. The goal of the system is to count the number of food items per category and make the available through an API.

We have already implemented a very basic version of this system as a docker-compose application. These are the different services:

* **Kafka** - A Kafka message message bus that can be used for communication between components.
* **Datafeed** - The feed component. It will occasionally produce a message on the Kafka topic with the name `message`
* **Consumer** - Example skeleton component that will consume and have a simple implementation of a "data pipline" to process these messages.
* **API** - An API that can be used to return the current fully processed data
* **data** - The data folder that contains the SQLite database that holds the processed information.

An example message looks like this:

```json
{
    "food": "sandwich",
}
```

## Description of the assignment

The goal of this assignment is to implement a more mature and robust data pipeline. Consider things like observability, scalability and maintability.

* The API, datafeed and the SQLite database itself should not be modified. (The database should only be written to without changing the table structure.)
* The consumer should be improved as per the goal described above
* Please use any 3rd party library that you feel is a fit
* It is OK to add services to the docker-compose application



## Getting started

This assignment requires *docker* and *docker-compose* to be installed on your system.

To run the skeleton application open a terminal, go to the directory containing the files for this assignment and run the following command:

```sh
$ docker-compose up --build
```

If all goes well, after some time, you should see the following output:

```sh
...
kafka_1      | [2023-11-16 19:29:54,923] INFO [SocketServer listenerType=ZK_BROKER, nodeId=1001] Started socket server acceptors and processors (kafka.network.SocketServer)
kafka_1      | [2023-11-16 19:29:54,926] INFO Kafka version: 2.8.1 (org.apache.kafka.common.utils.AppInfoParser)
kafka_1      | [2023-11-16 19:29:54,926] INFO Kafka commitId: 839b886f9b732b15 (org.apache.kafka.common.utils.AppInfoParser)
kafka_1      | [2023-11-16 19:29:54,926] INFO Kafka startTimeMs: 1700162994923 (org.apache.kafka.common.utils.AppInfoParser)
kafka_1      | [2023-11-16 19:29:54,929] INFO [KafkaServer id=1001] started (kafka.server.KafkaServer)
kafka_1      | [2023-11-16 19:29:54,969] INFO [ReplicaFetcherManager on broker 1001] Removed fetcher for partitions Set(picture-0, message-0) (kafka.server.ReplicaFetcherManager)
kafka_1      | [2023-11-16 19:29:54,973] INFO [Partition picture-0 broker=1001] Log loaded for partition picture-0 with initial high watermark 15 (kafka.cluster.Partition)
kafka_1      | [2023-11-16 19:29:54,976] INFO [Partition message-0 broker=1001] Log loaded for partition message-0 with initial high watermark 8249 (kafka.cluster.Partition)
kafka_1      | [2023-11-16 19:29:55,001] INFO [broker-1001-to-controller-send-thread]: Recorded new controller, from now on will use broker 87eb7706e27c:9092 (id: 1001 rack: null) (kafka.server.BrokerToControllerRequestThread)
consumer_1   | Kafka broker kafka:9092 appears not to be running yet, waiting 5 seconds before reconnecting
api_1        | 172.20.0.1 - - [16/Nov/2023 19:29:56] "GET /aggregated HTTP/1.1" 200 -
datafeed_1   | .. producer connected.
datafeed_1   | Sending random message {'food': 'broth'}...
datafeed_1   | Waiting 2 seconds...
consumer_1   | .. consumer connected.
datafeed_1   | Sending random message {'food': 'mayo'}...
datafeed_1   | Waiting 1 seconds...
consumer_1   | Received a message on topic message: {'food': 'mayo'}
datafeed_1   | Sending random message {'food': 'butter'}...
datafeed_1   | Waiting 1 seconds...
consumer_1   | Received a message on topic message: {'food': 'butter'}
datafeed_1   | Sending random message {'food': 'crumble'}...
datafeed_1   | Waiting 2 seconds...
consumer_1   | Received a message on topic message: {'food': 'crumble'}
datafeed_1   | Sending random message {'food': 'chocolate'}...
datafeed_1   | Waiting 1 seconds...

...
```

If you do not have this installed yet, use the following instructions:

#### Ubuntu

```sh
$ sudo apt-get update
$ sudo apt-get install docker.io docker-compose
```

#### Windows

Install the Docker Toolbox using the instructions on https://docs.docker.com/toolbox/toolbox_install_windows/

## Running from outside of the docker container

When developing it is often more convenient to run your code from outside of the Docker container. To support this, the Kafka container exposes two ports 9092 (for internal access) and 9094 (for external access and local development). When running locally you can configure the consumer to access port 9094 by setting the `KAFKA_BROKER` environment variable like this: 

```sh
# From within the consumer subdirectory
$ KAFKA_BROKER=localhost:9094 poetry run python consumer/main.py
```

## Troubleshooting
If for some reason the Kafka data gets corrupted, and sending / receiving of messages is no longer working then clear the Kafka database by running the following from the root of the codebase:

```sh
$ docker-compose rm
```
