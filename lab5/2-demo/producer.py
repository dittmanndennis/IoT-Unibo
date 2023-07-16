from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
import time
import json
import random

# Kafka cluster configuration
brokers = ['localhost:9091', 'localhost:9092', 'localhost:9093']

# Create the class for administrate Kafka cluster
admin_client = KafkaAdminClient(
    bootstrap_servers=brokers,
    client_id='test'
)
try:
    topic = "temperatures"
    new_topic = NewTopic(name=topic,
                         num_partitions=2, replication_factor=3)
    admin_client.create_topics(new_topics=[new_topic], validate_only=False)
except:
    print("error creating topic: prob already exits")


# Create the Kafka producer
producer = KafkaProducer(key_serializer=str.encode, value_serializer=lambda v: json.dumps(
    v).encode('utf-8'), bootstrap_servers=brokers)

num_sensors = 10
while True:
    for sensor in range(num_sensors):
        data = {"value": random.randint(0, 20)}
        id = f"temp-sensor:{sensor}"
        print(f"{id}: {data}")
        producer.send(topic, key=id, value=data)
        producer.flush()
        time.sleep(1)
