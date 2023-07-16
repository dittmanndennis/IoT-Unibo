import json

import paho.mqtt.client as mqtt_client

temp = []
hum = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("unibo/iot/dennis/test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    reading = json.loads(msg.payload)
    print(reading)
    print(type(reading))
    #reading = json.loads(reading)
    #print(reading)
    #print(type(reading))
    print(reading["sampling_rate"])
    #print(reading["calibration"])
    #print(reading["alarm_level"])
    #print(reading["alarm_counter"])

client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.username_pw_set("iot2020", password="mqtt2020*")

client.connect("broker.hivemq.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
