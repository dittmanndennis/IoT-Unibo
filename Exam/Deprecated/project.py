import logging
import asyncio
import time
import json

from aiocoap import *
from aiocoap.numbers.codes import GET

import paho.mqtt.client as mqtt_client

logging.basicConfig(level=logging.INFO)

sampling_rate = 20
calibration = 0
alarm_level = 200
alarm_counter = 3

temperature = []
humidity = []
weight = []
rssi = []
alarms = 0

delay_coap = []
delay_mqtt = []

async def main():
    global sampling_rate
    global calibration
    global alarm_level
    global alarm_counter

    global temperature
    global humidity
    global weight
    global rssi
    global alarms
    
    global delay_coap
    global delay_mqtt

    protocol = await Context.create_client_context()

    request_temp = Message(code=GET, uri='coap://130.136.2.70/temp:5683')
    request_hum = Message(code=GET, uri='coap://130.136.2.70/hum:5683')
    request_weight = Message(code=GET, uri='coap://130.136.2.70/weight:5683')
    request_rssi = Message(code=GET, uri='coap://130.136.2.70/rssi:5683')

    try:
        req_time = time.time()
        response_temp = await protocol.request(request_temp).response
        response_hum = await protocol.request(request_hum).response
        response_weight = await protocol.request(request_weight).response
        response_rssi = await protocol.request(request_rssi).response
    except Exception as e:
        print('Failed to fetch resource: ', e)
    else:
        print('Result: %s\n%r'%(response_temp.code, response_temp.payload))
        print('Result: %s\n%r'%(response_hum.code, response_hum.payload))
        print('Result: %s\n%r'%(response_weight.code, response_weight.payload))
        print('Result: %s\n%r'%(response_rssi.code, response_rssi.payload))
        
        delay_coap.append(time.time()-req_time)
        temperature.append(float(response_temp.payload))
        humidity.append(float(response_hum.payload))
        weight.append(float(response_weight.payload) - calibration)
        rssi.append(float(response_rssi.payload))
        if float(response_weight.payload) - calibration < alarm_level:
            alarms += 1
    
    if alarms >= alarm_counter:
        pub_time = time.time()
        client.publish("unibo/iot/dennis/alarm", payload=json.dumps({ 'water_weight': float(response_weight.payload) - calibration, 'rssi': float(response_rssi.payload) }))
        delay_mqtt.append(time.time()-pub_time)
    else:
        pub_time = time.time()
        client.publish("unibo/iot/dennis/regular", payload=json.dumps({ 'water_weight': float(response_weight.payload) - calibration, 'rssi': float(response_rssi.payload) }))
        delay_mqtt.append(time.time()-pub_time)

    if len(temperature) == sampling_rate:
        print("Mean delay CoAP: ", str(sum(delay_coap)/len(delay_coap)))

        print("Mean delay MQTT: ", str(sum(delay_mqtt)/len(delay_mqtt)))

        temperature = []
        humidity = []
        weight = []
        alarms = 0
        delay_coap = []
        if len(delay_mqtt) == 20:
            delay_mqtt = []


    time.sleep(sampling_rate)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("unibo/iot/dennis/config")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global sampling_rate
    global calibration
    global alarm_level
    global alarm_counter

    config = json.loads(msg.payload)

    sampling_rate = config["sampling_rate"]
    calibration = config["calibration"]
    alarm_level = config["alarm_level"]
    alarm_counter = config["alarm_counter"]

client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)

client.loop_forever()

if __name__ == "__main__":
    while True:
        asyncio.run(main())
