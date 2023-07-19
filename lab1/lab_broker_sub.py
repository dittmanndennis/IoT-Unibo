import paho.mqtt.client as mqtt_client

temp = []
hum = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensor/alarm")
    client.subscribe("sensor/regular")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "sensor/alarm":
        print("Alert: ", msg.payload)
    if msg.topic == "sensor/regular":
        print("Regular: ", msg.payload)

client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("iot2020", password="mqtt2020*")

client.connect("130.136.2.70", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
