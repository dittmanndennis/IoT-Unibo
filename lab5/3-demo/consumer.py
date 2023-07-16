from kafka import KafkaConsumer

# Kafka cluster configuration
brokers = ['localhost:9091', 'localhost:9092', 'localhost:9093']

# Create the Kafka consumer
topic = 'test-replication-4'
consumer = KafkaConsumer(topic, bootstrap_servers=brokers, auto_offset_reset='earliest')

# Consume events from the topic
for message in consumer:
    print(message.value.decode('utf-8'))

# Close the consumer connection
consumer.close()