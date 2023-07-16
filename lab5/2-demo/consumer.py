from kafka import KafkaConsumer

# Kafka cluster configuration
brokers = ['localhost:9091', 'localhost:9092', 'localhost:9093']

# Create the Kafka consumer
topic = 'temperatures'
consumer = KafkaConsumer(topic, group_id="processor", bootstrap_servers=brokers, auto_offset_reset='latest')
print('here')
# Consume events from the topic
for message in consumer:
    print(message.value.decode('utf-8'))
    print(message.key.decode('utf-8'))

# Close the consumer connection
consumer.close()