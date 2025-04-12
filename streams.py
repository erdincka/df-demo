import logging
import httpx

from confluent_kafka import Producer, Consumer, KafkaError

import settings

logging.getLogger("httpx").setLevel(logging.WARNING)

CONSUMER_GROUP = "streams-consumer"
producer = Producer({"streams.producer.default.stream": settings.STREAM})
consumer = Consumer(
    {
        "group.id": CONSUMER_GROUP,
        "default.topic.config": {"auto.offset.reset": "earliest"},
    }
)


def produce(message: str):
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    settings.logger.debug(
        "Got message %s for Topic: %s:%s", message, settings.STREAM, settings.TOPIC
    )

    try:
        producer.produce(settings.TOPIC, message.encode("utf-8"))

    except Exception as error:
        settings.logger.warning(error)
        return False

    finally:
        producer.flush()

    return True


def consume():
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    settings.logger.debug("Stream: %s Topic: %s", settings.STREAM, settings.TOPIC)
    MAX_POLL_TIME = 30

    try:

        consumer.subscribe([f"{settings.STREAM}:{settings.TOPIC }"])

        while True:
            message = consumer.poll(timeout=MAX_POLL_TIME)

            if message is None:
                raise EOFError

            if not message.error():
                yield message.value().decode("utf-8")

            elif message.error().code() == KafkaError._PARTITION_EOF:
                settings.logger.debug("No more messages in topic: %s", settings.TOPIC)
                # ui.notify(f"No more messages in {topic}")
                raise EOFError
            # silently ignore other errors
            else:
                settings.logger.warning(message.error())

    except Exception as error:
        settings.logger.warning(error)

    finally:
        consumer.close()


def stream_metrics(stream: str, topic: str):
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    URL = f"https://localhost:8443/rest/stream/topic/info?path={stream}&topic={topic}"
    AUTH = settings.get_credentials()

    settings.logger.debug(f"Fetching metrics from {URL}...")

    with httpx.Client(verify=False) as client:
        response = client.get(URL, auth=AUTH, timeout=2.0)

        if response is None or response.status_code != 200:
            # possibly not connected or topic not populated yet, just ignore
            settings.logger.debug(response.text)
            settings.logger.warning(f"Failed to get topic stats for {topic}")

        else:
            metrics = response.json()
            settings.logger.debug(f"Received metrics: {metrics}")
            if not metrics["status"] == "ERROR":
                logging.debug(f"Found {metrics}")
                yield metrics
            else:
                settings.logger.warning(f"Error in metrics: {metrics['errors']}")
