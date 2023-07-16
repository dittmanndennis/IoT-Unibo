from kafka import KafkaProducer
import time
import random

# Kafka cluster configuration
brokers = ['localhost:9092']

# Create the Kafka producer
producer = KafkaProducer(bootstrap_servers=brokers)

topic = "example-27"
# Send each line as an event every second
while True:
    temperature = str(random.randint(15, 20))
    print(f'send data')
    producer.send(topic, temperature.encode('utf-8'))
    producer.flush()
    time.sleep(1)
