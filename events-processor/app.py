from confluent_kafka import Producer, Consumer, KafkaError
import snowplow_analytics_sdk.event_transformer
import snowplow_analytics_sdk.snowplow_event_transformation_exception
import json

kafka_consumer = Consumer({
    'bootstrap.servers': "kafka.confluent.svc.cluster.local:9092",
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
    'session.timeout.ms': 10000,  # 10 seconds
    'max.poll.interval.ms': 300000,
    'group.instance.id': 'unique-consumer-instance-id',  # Unique ID for each consumer instance
    'heartbeat.interval.ms': 3000  # 3 seconds
 })


kafka_producer = Producer({
    'bootstrap.servers': "kafka.confluent.svc.cluster.local:9092",
})

kafka_consumer.subscribe(['snowplow_enriched_good'])

print('Successfully connected producer and consumer')
import time
time.sleep(2)


# Check available topics
metadata = kafka_consumer.list_topics(timeout=10)
available_topics = metadata.topics
print('Available topics:', available_topics.keys())

# Check partition assignment
assignment = kafka_consumer.assignment()
print('Assigned partitions:', assignment)

# Wait for partition assignment if not assigned
while not assignment:
    print('Waiting for partition assignment...')
    time.sleep(5)
    assignment = kafka_consumer.assignment()

print('Final assigned partitions:', assignment)

while True:
    msg = kafka_consumer.poll(1.0)

    if msg is None:
        print('No Messages')
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(f"Consumer error: {msg.error()}")
            break

    event = msg.value().decode('utf-8')

    try:
        json_data = snowplow_analytics_sdk.event_transformer.transform(event)
        kafka_producer.poll(0)
        kafka_producer.produce('snowplow_json_event', json.dumps(json_data).encode('utf-8'))
        kafka_producer.flush()
        print(json_data)
    except snowplow_analytics_sdk.snowplow_event_transformation_exception.SnowplowEventTransformationException as e:
        for error_message in e.error_messages:
            print(f"Transformation error: {error_message}")
    except Exception as e:
        print(f"Unexpected error: {e}")

kafka_consumer.close()
