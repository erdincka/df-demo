# pip3 install --global-option=build_ext --global-option="--library-dirs=/opt/mapr/lib" --global-option="--include-dirs=/opt/mapr/include/" mapr-streams-python
import confluent_kafka


def kafka_producer(topic, bootstrap_servers, value):
    from confluent_kafka import Producer
    p = Producer({'streams.producer.default.stream': '/demo/mystream'})
    some_data_source= ["msg1", "msg2", "msg3"]
    for data in some_data_source:
        p.produce('test', data.encode('utf-8'))
        p.flush()


# p = Producer({'streams.producer.default.stream': '/streams/python-test-stream'})
