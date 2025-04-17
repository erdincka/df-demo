import logging
from kafka import KafkaProducer, KafkaConsumer

import settings

logging.getLogger("kafka.conn").setLevel(logging.WARNING)
logging.getLogger("kafka.sasl.plain").setLevel(logging.ERROR)

# Create producer and consumer as singleton
username, password = settings.get_credentials()

CONSUMER_GROUP = "kafka-consumer"

def publish(message: str) -> bool:
    # FIX: for testing
    return True
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    producer = KafkaProducer(
        api_version=(3, 9),
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username=username,
        sasl_plain_password=password,
    )

    settings.logger.debug("Publishing message: %s", message)

    try:
        producer.send(settings.TOPIC, message.encode("utf-8"))

    except Exception as error:
        settings.logger.warning(error)
        return False

    finally:
        producer.flush()
        producer.close()

    return True

# CONSUMER_CMD = f"/opt/mapr/kafka/current/bin/kafka-console-consumer.sh --bootstrap-server localhost --from-beginning --topic {settings.STREAM if settings.isStreams else settings.KWPS_STREAM}:{settings.TOPIC}"
def subscribe():
    settings.logger.setLevel(
        level=logging.DEBUG if settings.isDebugging else logging.INFO
    )

    consumer = KafkaConsumer(
        api_version=(3, 9),
        auto_offset_reset="earliest",
        # client_id=f"kafka-app-{uuid.uuid4()}",  # Unique client ID for each consumer
        # group_id=CONSUMER_GROUP,
        # group_id=f"kafka-consumer-{uuid.uuid4()}",  # Unique group ID for each consumer
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username=username,
        sasl_plain_password=password,
    )

    settings.logger.debug("Subscribing to topic: %s", settings.TOPIC)
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
            settings.logger.debug("Messages consumed: " + str(numMsgConsumed))

    except Exception as error:
        settings.logger.error(error)
    finally:
        consumer.close()
        settings.logger.debug("Consumer closed")
