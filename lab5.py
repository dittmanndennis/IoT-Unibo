from kafka import KafkaConsumer

# Kafka cluster configuration
brokers = ['192.168.43.5:9092']

topic = 'exercise-1'
consumer = KafkaConsumer(topic, bootstrap_servers=brokers)

# Conusume events from the topic
for message in consumer:
    print(message.value.decode('utf-8'))

consumer.close()
