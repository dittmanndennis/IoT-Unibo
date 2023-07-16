from kafka import KafkaConsumer

# Kafka cluster configuration
brokers = [ 'localhost:9092']

# Create the Kafka consumer
topic = 'example-27'
consumer = KafkaConsumer(topic, bootstrap_servers=brokers)

# Consume events from the topic
for message in consumer:
    print(message.value.decode('utf-8'))

# Close the consumer connection
consumer.close()