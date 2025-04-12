import logging
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
    group_id="kafka-consumer-group2",
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username=username,
    sasl_plain_password=password,
)


def publish(message: str) -> bool:
    settings.logger.debug("Sending: %s", message)

    try:
        producer.send(settings.TOPIC, message.encode("utf-8"))

    except Exception as error:
        settings.logger.warning(error)
        return False

    finally:
        producer.flush()

    return True


def subscribe():

    try:
        consumer.subscribe([settings.TOPIC])

        numMsgConsumed = 0
        records = consumer.poll(timeout_ms=1000)
        print(records)
        for topic_data, consumer_records in records.items():
            for consumer_record in consumer_records:
                yield str(consumer_record.value.decode("utf-8"))
                numMsgConsumed += 1
        settings.logger.info("Messages consumed: " + str(numMsgConsumed))
        # consumer.commit_async(callback=settings.logger.warning)

    except Exception as error:
        settings.logger.warning(error)


if __name__ == "__main__":
    # print(publish(f"Test {datetime.datetime.now().timestamp()}"))
    for msg in subscribe():
        print(msg)
