from concurrent.futures import ThreadPoolExecutor
import os
import logging
import httpx

os.environ["LD_LIBRARY_PATH"] = "/opt/mapr/lib:/usr/lib/jvm/java-11-openjdk-11.0.24.0.8-3.el8.x86_64/lib/server/libjvm.so"

from confluent_kafka import Producer, Consumer, KafkaError

logger = logging.getLogger(__name__)

CONSUMER_GROUP= "devices-app"

def produce(stream: str, topic: str, message: str):

    logger.debug("Stream path: %s", stream)
    p = Producer({"streams.producer.default.stream": stream})

    try:
        logger.info("sending message: %s", message)
        p.produce(topic, message.encode("utf-8"))

    except Exception as error:
        logger.warning(error)
        return False

    finally:
        p.flush()

    return True


def consume(stream: str, topic: str):

    logger.info("Stream: %s Topic: %s", stream, topic)
    MAX_POLL_TIME = 30

    consumer = Consumer(
        {"group.id": CONSUMER_GROUP, "default.topic.config": {"auto.offset.reset": "earliest"}}
    )

    try:

        consumer.subscribe([f"{stream}:{topic}"])

        while True:
            message = consumer.poll(timeout=MAX_POLL_TIME)

            if message is None: raise EOFError

            if not message.error(): yield message.value().decode("utf-8")

            elif message.error().code() == KafkaError._PARTITION_EOF:
                logger.info("No more messages in topic: %s", topic)
                # ui.notify(f"No more messages in {topic}")
                raise EOFError
            # silently ignore other errors
            else: logger.warning(message.error())

    except Exception as error:
        logger.warning(error)

    finally:
        consumer.close()


async def stream_metrics(stream: str, topic: str):
    URL = f"https://localhost:8443/rest/stream/topic/info?path={stream}&topic={topic}"
    AUTH = ("mapr", "mapr")
    logger.debug(URL)

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(URL, auth=AUTH, timeout=2.0)

        if response is None or response.status_code != 200:
            # possibly not connected or topic not populated yet, just ignore
            logger.info(response.text)
            logger.warning(f"Failed to get topic stats for {topic}")

        else:
            metrics = response.json()
            if not metrics["status"] == "ERROR":
                logging.debug(f"Found {metrics}")
                yield metrics
