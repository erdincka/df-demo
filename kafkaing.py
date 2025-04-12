import logging
import uuid
from kafka import KafkaProducer, KafkaConsumer

import settings

logging.getLogger("kafka.conn").setLevel(logging.WARNING)
logging.getLogger("kafka.sasl.plain").setLevel(logging.ERROR)

# Create producer and consumer as singleton
username, password = settings.get_credentials()

producer = KafkaProducer(
    api_version=(3, 6),
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username=username,
    sasl_plain_password=password,
)

consumer = KafkaConsumer(
    api_version=(3, 6),
    auto_offset_reset="earliest",
    # client_id="kafka-app-consumer",
    group_id="kafka-consumer-group",
    # group_id=f"kafka-consumer-group-{uuid.uuid4()}",  # Unique group ID for each consumer
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username=username,
    sasl_plain_password=password,
)


def publish(message: str) -> bool:
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    settings.logger.debug("Publishing message: %s", message)

    try:
        producer.send(settings.TOPIC, message.encode("utf-8"))

    except Exception as error:
        settings.logger.warning(error)
        return False

    finally:
        producer.flush()

    return True


def subscribe():
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    settings.logger.debug("Subscribing to topic: %s", settings.TOPIC)
    numMsgConsumed = 0
    try:
        consumer.subscribe([settings.TOPIC])

        records = consumer.poll(timeout_ms=1000)

        for topic_data, consumer_records in records.items():
            for consumer_record in consumer_records:
                yield str(consumer_record.value.decode("utf-8"))
                numMsgConsumed += 1
        settings.logger.info("Messages consumed: " + str(numMsgConsumed))

    except Exception as error:
        settings.logger.warning(error)


if __name__ == "__main__":
    # print(publish(f"Test {datetime.datetime.now().timestamp()}"))
    for msg in subscribe():
        print(msg)
