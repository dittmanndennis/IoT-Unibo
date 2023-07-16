from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic, ConfigResource
import time
import os


# Kafka cluster configuration
brokers = ['localhost:9091', 'localhost:9092', 'localhost:9093']

# Create the class for administrate Kafka cluster
admin_client = KafkaAdminClient(
    bootstrap_servers=brokers,
    client_id='test'
)

topic = f"test-replication-4"
try:
    new_topic = NewTopic(name=topic,
                         num_partitions=1, replication_factor=1)
    admin_client.create_topics(new_topics=[new_topic], validate_only=False)
except Exception as e:
    print("Error creating topic")
    print(e)


producer = KafkaProducer(bootstrap_servers=brokers)

i = 0
while True:
    i += 1
    producer.send(topic, str(i).encode('ascii'))
    producer.flush()
    time.sleep(1)

# Close the producer connection
producer.close()
