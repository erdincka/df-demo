import logging
from kafka import KafkaProducer
from kafka import KafkaConsumer
import sys

#Specify 'broker' and 'topic' arguments. Example: 'python3 saslPlaintestKafkaPythonClient.py localhost:9092 topicTestKafkaPythonClient_SASL'
server = sys.argv[1]
print("BROKER: " + server)
topic = sys.argv[2]
print("TOPIC: " + topic)

# Create logger for consumer (logs will be emitted when poll() is called)
logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)

#PRODUCER
# print("\n**Starting Producer**")
# producer=KafkaProducer(bootstrap_servers=[server],
#                         api_version=(3, 9),
#                         security_protocol='SASL_PLAINTEXT',
#                         sasl_mechanism='PLAIN',
#                         sasl_plain_username='mapr',
#                         sasl_plain_password='mapr')

# numMsgProduced = 0
# for _ in range(100):
#     producer.send(topic, b'msg')
#     numMsgProduced += 1
# producer.flush()
# print("Messages produced: " + str(numMsgProduced))
# time.sleep(2)

# CONSUMER
print("\n**Starting Consumer**")
# consumer = KafkaConsumer(bootstrap_servers=[server],
#                         api_version=(3, 9),
#                         auto_offset_reset='earliest',
#                         group_id="kafka-consumer",
#                         security_protocol='SASL_PLAINTEXT',
#                         sasl_mechanism='PLAIN',
#                         sasl_plain_username='mapr',
#                         sasl_plain_password='mapr')

# consumer.subscribe([topic])
# numMsgConsumed = 0
# for _ in range(10):
#     records = consumer.poll(timeout_ms=500)
#     for topic_data, consumer_records in records.items():
#         for consumer_record in consumer_records:
#             print("Received message: " + str(consumer_record.value.decode('utf-8')))
#             numMsgConsumed += 1
# print("Messages consumed: " + str(numMsgConsumed))


from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': server,
    'group.id': 'kafka-consumer',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'mapr',
    'sasl.password': 'mapr',
    'auto.offset.reset': 'earliest'
}
c = Consumer(conf)
c.subscribe([topic])

try:

    while True:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print(msg.error())

        else:
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
            print(msg.value())

except KeyboardInterrupt:
    sys.stderr.write("%% Aborted by user\n")
finally:
    c.close()
