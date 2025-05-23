import logging
from kafka import KafkaProducer, KafkaConsumer

import settings

logging.getLogger("kafka.conn").setLevel(logging.WARNING)
logging.getLogger("kafka.sasl.plain").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Create producer and consumer as singleton
username, password = settings.get_credentials()

CONSUMER_GROUP = "kafka-consumer"

producer = KafkaProducer(
    bootstrap_servers=["maprdemo.io:9092"],
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username=username,
    sasl_plain_password=password,
)

consumer = KafkaConsumer(
    bootstrap_servers=["maprdemo.io:9092"],
    auto_offset_reset="earliest",
    group_id=CONSUMER_GROUP,
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username=username,
    sasl_plain_password=password,
)


def publish(message: str) -> bool:

    logger.debug("Publishing message: %s", message)

    try:
        producer.send(settings.TOPIC, message.encode("utf-8"))

    except Exception as error:
        logger.warning(error)
        return False

    finally:
        producer.flush()
        producer.close()

    return True


def subscribe():
    logger.debug("Subscribing to topic: %s", settings.TOPIC)
    numMsgConsumed = 0
    try:
        consumer.subscribe([settings.TOPIC])

        while True:
            records = consumer.poll(timeout_ms=1000)

            for topic_data, consumer_records in records.items():
                for consumer_record in consumer_records:
                    numMsgConsumed += 1
                    yield str(consumer_record.value.decode("utf-8"))
            if not numMsgConsumed > 0: break # Break the loop if no messages are consumed in the last iteration
            logger.debug("Messages consumed: " + str(numMsgConsumed))

    except Exception as error:
        logger.error(error)
    finally:
        logger.debug("Consumer closed")
        consumer.close()


