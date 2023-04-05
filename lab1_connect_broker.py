import paho.mqtt.client as mqtt_client

temp = []
hum = []

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensor/temp")
    client.subscribe("sensor/hum")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global temp
    global hum
    reading = float(msg.payload)
    if msg.topic == "sensor/temp":
        if len(temp) == 4:
            temp.append(reading)
            print(sum(temp) / len(temp))
            print(min(temp))
            if sum(temp) / len(temp) > 24:
                client.publish("sensor/alert", payload="temperature to high")
                print("temp sent")
            temp = []
        else:
            print("New temp: "+str(reading))
            temp.append(reading)
    if msg.topic == "sensor/hum":
        if len(hum) == 4:
            hum.append(reading)
            print(sum(hum) / len(hum))
            print(max(hum))
            if sum(hum) / len(hum) > 27:
                client.publish("sensor/alert", payload="humidity to high")
                print("hum sent")
            hum = []
        else:
            print("New hum: "+str(reading))
            hum.append(reading)

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
